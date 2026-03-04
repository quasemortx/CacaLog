import logging
import os
import re
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.sheets import SheetsClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cacalog")

# Constants from parser logic
ALWAYS_MODELS = {"390", "5040", "7020", "7040"}
AMBIGUOUS_NUMBERS = {"3010", "3020"}
BRANDS = {"LENOVO", "HP", "XPS", "DELL"}


def extract_model_from_text(text: str) -> str | None:
    """
    Extracts explicit model or brand from text.
    Prioritizes specific numbers (e.g. 3020) over generic brands.
    """
    if not text:
        return None
    t_upper = text.upper()

    # Check specific numbers first (Optiplex usually)
    # Combine lists
    all_nums = ALWAYS_MODELS.union(AMBIGUOUS_NUMBERS)
    for num in all_nums:
        # Regex for word boundary
        if re.search(rf"\b{num}\b", t_upper):
            return f"OptiPlex {num}"  # Standardize naming

    # Regex checks for Brands (Safer than 'in')
    # HP: \bHP\b matches " HP " but not "PHP"
    if re.search(r"\bHP\b", t_upper):
        return "HP"
    if re.search(r"\bXPS\b", t_upper):
        return "XPS"

    # Lenovo logic
    if "LENOVO" in t_upper:
        if "MINI" in t_upper:
            return "Lenovo Mini"
        return "Lenovo"

    # Generic "Optiplex" without number?
    if "OPTIPLEX" in t_upper:
        return "OptiPlex Generic"

    return None


def main():
    logger.info("Initializing Sheets Client...")
    sheets = SheetsClient()
    ws = sheets.inventory_ws

    logger.info("Fetching all records...")
    records = ws.get_all_records()  # Returns list of dicts

    if not records:
        logger.warning("No records found.")
        return

    updates = []

    # We need to write back to specific cells.
    # gspread's update_cells or parsing the whole data range is better.
    # Let's get header map to known column index for `update`.
    # Using `get_all_values` is safer for index-based updates.

    all_values = ws.get_all_values()
    headers = all_values[0]

    try:
        idx_obs = headers.index("Observacao")
        idx_modelo = headers.index("Modelo")
        idx_local = headers.index("local_id")
    except ValueError:
        logger.error("Required columns missing.")
        return

    updated_count = 0

    # Iterate data rows
    for i in range(1, len(all_values)):
        row = all_values[i]

        obs = row[idx_obs]
        current_model = row[idx_modelo]

        # Only update if Model is currently empty (or maybe we assume obs is fresher? User said "Atualize checking obs")
        # Let's trust Obs if Model is empty.
        if not current_model.strip():
            extracted = extract_model_from_text(obs)
            if extracted:
                logger.info(f"Found model '{extracted}' in obs '{obs}' for {row[idx_local]}")
                row[idx_modelo] = extracted
                updated_count += 1

    if updated_count > 0:
        logger.info(f"Updating {updated_count} rows...")
        ws.update(range_name="A1", values=all_values)
        logger.info("Sheet updated successfully.")
    else:
        logger.info("No missing models found in observations.")


if __name__ == "__main__":
    main()
