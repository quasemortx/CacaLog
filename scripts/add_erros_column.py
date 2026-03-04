import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.sheets import SheetsClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mig_erros")


def main():
    logger.info("Initializing Sheets Client...")
    sheets = SheetsClient()
    ws = sheets.inventory_ws

    logger.info("Fetching all records (values)...")
    all_values = ws.get_all_values()
    if not all_values:
        return

    headers = all_values[0]

    # Check if Erros exists
    if "Erros" in headers:
        logger.info("'Erros' column already exists.")
        return
    else:
        # We need to INSERT it at position 10 (after Pendentes)
        # Headers: ..., Concluidos(8), Pendentes(9), [Erros(10)], Status(11)...

        logger.info("Inserting 'Erros' column at index 10...")

        # Insert in Header
        headers.insert(10, "Erros")

        # Insert in all rows
        for i in range(1, len(all_values)):
            # Pad row if short
            while len(all_values[i]) < 10:
                all_values[i].append("")
            # Insert 0 as default
            all_values[i].insert(10, "0")

    logger.info("Updating sheet structure...")
    ws.clear()
    ws.update(range_name="A1", values=all_values)
    logger.info("Sheet structure updated successfully.")


if __name__ == "__main__":
    main()
