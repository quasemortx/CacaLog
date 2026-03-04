import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.sheets import SheetsClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("audit")


def main():
    sheets = SheetsClient()
    logger.info("Fetching all records...")
    records = sheets.inventory_ws.get_all_records()

    missing_models_count = 0
    print("\n--- Rows with Empty Model but non-empty Observation ---\n")

    for r in records:
        model = str(r.get("Modelo", "")).strip()
        obs = str(r.get("Observacao", "")).strip()
        local_id = r.get("local_id", "Unknown")

        if not model and obs:
            missing_models_count += 1
            print(f"[{local_id}] Obs: {obs}")

    print(f"\nTotal potential candidates: {missing_models_count}")


if __name__ == "__main__":
    main()
