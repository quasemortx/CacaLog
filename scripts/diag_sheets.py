from app.sheets import SheetsClient

def diagnostic():
    client = SheetsClient()
    records = client.get_all_records()
    
    p1_records = []
    for r in records:
        p = str(r.get('Predio', '')).upper()
        if '1' in p:
            p1_records.append(r)
            
    print(f"Total P1 records: {len(p1_records)}")
    
    zero_pcs = [r for r in p1_records if not r.get('TotalPCs') or int(r.get('TotalPCs')) == 0]
    print(f"Records in P1 with 0 or empty TotalPCs: {len(zero_pcs)}")
    
    if zero_pcs:
        print("\nIDs with 0 TotalPCs (sample 10):")
        for r in zero_pcs[:10]:
            print(f"  - {r.get('local_id')}: Tipo={r.get('TipoAmbiente')}, Predio={r.get('Predio')}")

    # Check for P1 Labs specifically
    labs = [r for r in records if r.get('TipoAmbiente') == 'LAB']
    print(f"\nTotal Labs in all spreadsheet: {len(labs)}")
    for l in labs:
        print(f"  - {l.get('local_id')}: Predio={l.get('Predio')}")

if __name__ == "__main__":
    diagnostic()
