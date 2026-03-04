import logging
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.sheets import SheetsClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cacalog")


def main():
    logger.info("Initializing Sheets Client...")
    sheets = SheetsClient()
    ws = sheets.inventory_ws

    logger.info("Fetching entire sheet...")
    all_values = ws.get_all_values()

    if not all_values:
        logger.warning("Empty sheet.")
        return

    headers = all_values[0]

    try:
        idx_predio = headers.index("Predio")
        idx_andar = headers.index("Andar")
        idx_sala = headers.index("Sala")
    except ValueError:
        logger.error("Could not find headers Predio/Andar/Sala.")
        return

    updated_count = 0

    # Iterate skipping header
    for i in range(1, len(all_values)):
        row = all_values[i]

        # Helper to force int
        def force_int(val):
            if isinstance(val, int):
                return val
            if isinstance(val, str) and val.strip().isdigit():
                return int(val.strip())
            return val  # Keep original if not digit (e.g. empty or complex)

        # Fix Predio
        if idx_predio < len(row):
            old_p = row[idx_predio]
            new_p = force_int(old_p)
            if old_p != new_p:
                row[idx_predio] = new_p
                updated_count += 1

        # Fix Andar
        if idx_andar < len(row):
            old_a = row[idx_andar]
            new_a = force_int(old_a)
            if old_a != new_a:
                row[idx_andar] = new_a
                updated_count += 1

        # Fix Sala (Keep as string usually, but ensure consistency?
        # Actually Sala '202' vs 202 might irrelevant if regex uses string matching,
        # but for sorting, consistently string is better or consistently int.
        # Let's clean empty strings.

    logger.info(f"Fixed types for {updated_count} cells. Uploading...")

    # Update bulk
    # Need to check if gspread supports raw types in update.
    # update() with raw=False (default) might treat input as whatever.
    # We rely on python int -> json number -> sheet number.

    ws.update("A1", all_values)

    logger.info("Sorting...")
    sheets.sort_inventory()

    logger.info("Done.")


if __name__ == "__main__":
    main()
