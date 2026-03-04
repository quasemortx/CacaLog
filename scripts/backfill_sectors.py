import sys
import os
import logging

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.sheets import SheetsClient
from app.utils import classify_sector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backfill_sector")

def main():
    logger.info("Initializing Sheets Client...")
    sheets = SheetsClient()
    ws = sheets.inventory_ws
    
    logger.info("Fetching all records (values)...")
    all_values = ws.get_all_values()
    if not all_values: return
    
    headers = all_values[0]
    
    # Check if Setor exists
    if "Setor" in headers:
        idx_setor = headers.index("Setor")
        logger.info(f"'Setor' column found at index {idx_setor}.")
    else:
        # We need to INSERT it at position 12 (after Observacao)
        logger.info("Inserting 'Setor' column at index 12...")
        # Target Header Structure: ... Status(10), Observacao(11), Setor(12), UltimoResponsavel(13) ...
        # Current: ... Observacao(11), UltimoResponsavel(12) ...
        
        # Insert in Header
        headers.insert(12, "Setor")
        
        # Insert in all rows
        for i in range(1, len(all_values)):
            # Pad row if short
            while len(all_values[i]) < 12:
                all_values[i].append("")
            # Insert empty/calc value
            all_values[i].insert(12, "")
            
        idx_setor = 12

    try:
        idx_status = headers.index("Status")
        idx_obs = headers.index("Observacao")
    except ValueError:
        logger.error("Missing Status/Observacao columns.")
        return

    updated_count = 0
    
    # Recalculate Logic
    for i in range(1, len(all_values)):
        row = all_values[i]
        
        # Safety check length
        if len(row) <= idx_status or len(row) <= idx_obs: continue
        
        status = row[idx_status]
        obs = row[idx_obs]
        current_val = row[idx_setor]
        
        new_val = classify_sector(status, obs)
        
        if new_val != current_val:
            row[idx_setor] = new_val
            updated_count += 1
            
    if updated_count > 0 or "Setor" not in headers: # Save if we updated rows OR structure
        logger.info(f"Updating sheet (Structure+Values)... {updated_count} rows changed.")
        ws.clear() # Safer to clear and rewrite for structure change
        ws.update(range_name="A1", values=all_values)
        logger.info("Sheet structure and data updated.")
    else:
        logger.info("No changes needed.")

if __name__ == "__main__":
    main()
