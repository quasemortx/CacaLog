import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.sheets import SheetsClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("debug_cmd")

def main():
    sheets = SheetsClient()
    logger.info("Fetching all records...")
    records = sheets.inventory_ws.get_all_records()
    
    if not records:
        print("No records found.")
        return

    print(f"Total Records: {len(records)}")
    if records:
        print(f"Sample Record Keys: {list(records[0].keys())}")
        
    target_sector = "TI"
    
    # Debug Filter
    found = []
    print("\n--- Scanning for TI candidates ---")
    for r in records:
        status = r.get('Status', 'UNKNOWN')
        setor = r.get('Setor', 'N/A')
        local = r.get('local_id', '?')
        obs = r.get('Observacao', '')
        
        # Check condition
        is_candidates = status != 'OK' and setor == target_sector
        
        if is_candidates:
             found.append(r)
             print(f"[MATCH] {local} | Status: {status} | Setor: {setor}")
        elif setor == target_sector:
             print(f"[MISS - Status OK?] {local} | Status: {status} | Setor: {setor}")
        elif "TI" in str(setor).upper():
             print(f"[MISS - mismatch?] {local} | Setor: '{setor}' vs 'TI' ")
             
    print(f"\nTotal TI Found: {len(found)}")

if __name__ == "__main__":
    main()
