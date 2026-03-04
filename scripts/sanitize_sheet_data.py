import sys
import os
import logging

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.sheets import SheetsClient
from app.utils import sanitize_for_sheets
from app.parser import normalize_status
from app.models import Status

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cacalog")

def main():
    print("Initializing Sheets Client...")
    try:
        sheets = SheetsClient()
        ws = sheets.inventory_ws
        
        print("Fetching all values...")
        all_values = ws.get_all_values()
        
        if not all_values:
            print("Sheet is empty.")
            return

        headers = all_values[0]
        try:
            obs_index = headers.index("Observacao")
            status_index = headers.index("Status")
        except ValueError:
            print("Required columns 'Observacao' or 'Status' not found.")
            return

        print(f"Columns: Observacao={obs_index}, Status={status_index}")
        
        updates_made = 0
        
        # Start from row 2 (index 1)
        for i, row in enumerate(all_values[1:], start=2):
            # 1. Sanitize Observation
            if obs_index < len(row):
                original_obs = row[obs_index]
                sanitized_obs = sanitize_for_sheets(original_obs)
                if original_obs != sanitized_obs:
                    row[obs_index] = sanitized_obs
                    updates_made += 1
            
            # 2. Migrate Status (NAO_AVALIADO -> ATUALIZANDO based on obs)
            if status_index < len(row):
                current_status = row[status_index]
                obs_lower = row[obs_index].lower()
                
                if current_status == "NAO_AVALIADO":
                    # Check keywords manually or use parser logic
                    if any(x in obs_lower for x in ['atualizando', 'verificando', '🔄', 'aguarde']):
                        print(f"Row {i}: Migrating Status -> ATUALIZANDO")
                        row[status_index] = "ATUALIZANDO"
                        updates_made += 1

        print(f"Total cell updates prepared: {updates_made}")
        
        print("Writing data back to sheet...")
        ws.update(range_name=f"A1", values=all_values)
        
        print("Sorting inventory...")
        sheets._sort_inventory()
        
        print("Update complete (Sanitization + Migration + Sort).")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    main()
