import asyncio
import re
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.sheets import SheetsClient
from app.parser import extract_data_regex, normalize_status, Status
from app.models import InventoryItem, TipoAmbiente

# Path to the specific log file
LOG_FILE = "../Conversa do WhatsApp com SEOP.txt"
MSG_REGEX = re.compile(r'^(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - ([^:]+): (.*)$', re.DOTALL)

async def update_database():
    print("🚀 Starting Database Update (SEOP Log)...")
    
    # 1. Initialize Sheets Client
    try:
        sheets = SheetsClient()
        print("✅ Sheets Client Initialized.")
    except Exception as e:
        print(f"❌ Failed to initialize Sheets: {e}")
        return

    # 2. Load CURRENT Sheet State (To preserve existing data)
    print("📥 Loading current inventory from Sheets...")
    current_records = sheets.get_all_records()
    inventory_state = {}
    
    # Convert list of dicts to dict of InventoryItem objects
    # This allows us to modify existing items easily
    for r in current_records:
        lid = str(r.get('local_id', ''))
        if not lid: continue
        
        # Map sheet headers to model fields
        # Note: headers in sheets.py are capitalized (Sala, Predio...)
        # But get_all_records returns dict keys as they are in sheet (usually capitalized)
        
        # Helper to safely get int
        def safe_int(val, default=0):
            try: return int(val)
            except: return default

        item = InventoryItem(
            local_id=lid,
            sala=str(r.get('Sala', '')),
            predio=safe_int(r.get('Predio')),
            andar=safe_int(r.get('Andar')),
            tipo_ambiente=TipoAmbiente(r.get('TipoAmbiente', 'SALA')), # Default fallback
            modelo=str(r.get('Modelo', '')),
            bios=str(r.get('BIOS', '')),
            total_pcs=safe_int(r.get('TotalPCs')),
            concluidos=safe_int(r.get('Concluidos')),
            pendentes=safe_int(r.get('Pendentes')),
            erros=safe_int(r.get('Erros')),
            status=normalize_status(r.get('Status', 'NAO_AVALIADO')),
            observacao=str(r.get('Observacao', '')),
            setor_responsavel=str(r.get('Setor', '')),
            ultimo_responsavel=str(r.get('UltimoResponsavel', '')),
            ultimo_contato=str(r.get('UltimoContato', '')),
            ultima_atualizacao=str(r.get('UltimaAtualizacao', ''))
        )
        inventory_state[lid] = item
        
    print(f"📊 Loaded {len(inventory_state)} existing items.")

    # 3. Read Log File
    if not os.path.exists(LOG_FILE):
        print(f"❌ Log file not found: {LOG_FILE}")
        return
        
    print(f"📂 Reading {LOG_FILE}...")
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Reconstruct messages
    messages = []
    current_msg = None
    lines = content.split('\n')
    for line in lines:
        match = MSG_REGEX.match(line)
        if match:
            if current_msg: messages.append(current_msg)
            timestamp, sender, body = match.groups()
            current_msg = {"timestamp": timestamp, "sender": sender, "body": body}
        else:
            if current_msg: current_msg["body"] += "\n" + line.strip()
    if current_msg: messages.append(current_msg)
        
    print(f"📨 Found {len(messages)} new messages to process.")
    
    # 4. Update State with New Log Info
    print("⚙️ Processing updates...")
    updates_count = 0
    new_items_count = 0
    
    for msg in messages:
        body = msg["body"]
        sender = msg["sender"]
        timestamp = msg["timestamp"]
        
        extracted = extract_data_regex(body)
        if not extracted: continue
            
        for new_data in extracted:
            lid = new_data['local_id']
            
            is_new = lid not in inventory_state
            
            if is_new:
                # Create NEW item
                item = InventoryItem(
                    local_id=lid,
                    sala=new_data.get('sala'),
                    predio=new_data.get('predio'),
                    andar=new_data.get('andar'),
                    tipo_ambiente=new_data['tipo_ambiente'],
                    status=Status.NAO_AVALIADO,
                    observacao="",
                    ultimo_responsavel=sender,
                    ultima_atualizacao=timestamp
                )
                inventory_state[lid] = item
                new_items_count += 1
            else:
                item = inventory_state[lid]
                updates_count += 1
                
            # Apply Updates (Merge Logic)
            
            # Status
            new_status_val = new_data.get('status')
            if isinstance(new_status_val, str): new_status_val = normalize_status(new_status_val)
            if new_status_val and new_status_val != Status.NAO_AVALIADO:
                item.status = new_status_val
                
            # Model (only update if present)
            if new_data.get('modelo'):
                item.modelo = new_data['modelo']
                
            # Obs (Overwrite is standard for latest update)
            item.observacao = new_data.get('observacao', body)
            
            # Counts (for Labs)
            if new_data.get('tipo_ambiente') == TipoAmbiente.LAB:
                 if new_data.get('total_pcs') is not None: item.total_pcs = new_data['total_pcs']
                 if new_data.get('concluidos') is not None: item.concluidos = new_data['concluidos']
                 if new_data.get('pendentes') is not None: item.pendentes = new_data['pendentes']
                 if new_data.get('erros') is not None: item.erros = new_data['erros']
            
            # Metadata
            item.ultimo_responsavel = sender
            item.ultima_atualizacao = timestamp
            
            # Save back
            inventory_state[lid] = item

    print(f"📝 Processed updates: {updates_count} updates, {new_items_count} new items.")
    
    # 5. Batch Upload (Overwrite all rows with new state)
    # This is safe because we loaded the current state first.
    # Any item NOT in inventory_state (because it wasn't in sheet and wasn't in log) stays deleted.
    # Any item deleted manually by user is GONE from inventory_state (because it wasn't in sheet),
    # UNLESS the log mentions it, in which case it is resurrected (which is usually desired behavior for a log processor: "Hey, I found info about X").
    
    print(f"☁️ Uploading {len(inventory_state)} items to Google Sheets...")
    
    # Sort
    def get_sort_key(item):
        p = item.predio or 0
        a = item.andar or 0
        s = item.sala or ""
        return (p, a, s)
    sorted_items = sorted(inventory_state.values(), key=get_sort_key)
    
    rows = []
    for item in sorted_items:
        row = [
            item.local_id,
            item.sala,
            item.predio,
            item.andar,
            item.tipo_ambiente.value,
            item.modelo,
            item.bios,
            item.total_pcs,
            item.concluidos,
            item.pendentes,
            item.erros,
            item.status.value,
            item.observacao,
            item.setor_responsavel,
            item.ultimo_responsavel,
            item.ultimo_contato,
            item.ultima_atualizacao
        ]
        rows.append(row)
        
    try:
        # Clear data range but keep headers?
        # Actually, let's just clear A2:Q and write fresh.
        # This ensures deleted rows at the bottom are removed.
        sheets.inventory_ws.batch_clear(["A2:Q10000"])
        
        if rows:
            end_row = 1 + len(rows)
            range_name = f"A2:Q{end_row}"
            sheets.inventory_ws.update(range_name=range_name, values=rows)
            print(f"✅ Successfully wrote {len(rows)} rows.")
        else:
            print("⚠️ No data to write.")
            
    except Exception as e:
         print(f"❌ Error during update: {e}")
         
    print("✅ Update Complete!")

if __name__ == "__main__":
    asyncio.run(update_database())
