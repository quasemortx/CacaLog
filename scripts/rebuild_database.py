import asyncio
import os
import re
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import InventoryItem, TipoAmbiente
from app.parser import Status, extract_data_regex, normalize_status
from app.sheets import SheetsClient

# Path to the specific log file
LOG_FILE = "../Conversa do WhatsApp com TROPA DA T.I.txt"

# Regex for WhatsApp timestamp and sender
# Example: 15/01/2026 10:15 - Patric Cortez: Body
MSG_REGEX = re.compile(r"^(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - ([^:]+): (.*)$", re.DOTALL)


async def rebuild_database():
    print("🚀 Starting Database Rebuild...")

    # 1. Initialize Sheets Client
    try:
        sheets = SheetsClient()
        print("✅ Sheets Client Initialized.")
    except Exception as e:
        print(f"❌ Failed to initialize Sheets: {e}")
        return

    # 2. Clear Existing Data (Optional/Risky? User said "limpe toda a planilha")
    # Let's assume we clear it.
    print("🧹 Clearing 'Inventario' worksheet...")
    try:
        # Get all records to know range? Or just clear range A2:Z
        sheets.inventory_ws.batch_clear(["A2:Z10000"])
        print("✅ Worksheet cleared.")
    except Exception as e:
        print(f"❌ Failed to clear worksheet: {e}")
        return

    # 3. Read Log File
    if not os.path.exists(LOG_FILE):
        print(f"❌ Log file not found: {LOG_FILE}")
        return

    print(f"📂 Reading {LOG_FILE}...")
    with open(LOG_FILE, encoding="utf-8") as f:
        content = f.read()

    # The log file has multi-line messages. Reading line-by-line might break multi-line messages
    # if they are just separated by newlines within the message body.
    # However, WhatsApp export usually keeps one message per line OR uses a specific format.
    # Looking at the provided log:
    # 30/01/2026 10:53 - J.F: Lab 05
    # 1 - win 11
    # 12 - win 10
    #
    # These are separate lines in the text file.
    # We need to reconstruct messages.
    # Strategy: A new message starts with Date/Time regex. Everything until next Date/Time is the body.

    messages = []
    current_msg = None

    lines = content.split("\n")
    for line in lines:
        match = MSG_REGEX.match(line)
        if match:
            # Save previous message
            if current_msg:
                messages.append(current_msg)

            # Start new message
            timestamp, sender, body = match.groups()
            current_msg = {"timestamp": timestamp, "sender": sender, "body": body}
        else:
            # Continuation of previous message body
            if current_msg:
                current_msg["body"] += "\n" + line.strip()

    # Append last message
    if current_msg:
        messages.append(current_msg)

    print(f"📊 Found {len(messages)} messages to process.")

    # 4. Parse and Upsert
    processed_count = 0

    # We want to process chronologically (Start to End).
    # The log seems chronological.

    for i, msg in enumerate(messages):
        body = msg["body"]
        sender = msg["sender"]
        timestamp = msg["timestamp"]

        # Parse
        items = extract_data_regex(body)

        if items:
            for item in items:
                # Merge Logic (Simplified for Rebuild: Just overwrite since we go chronological)
                # But we have Partial Update logic in main.py.
                # Should we reuse that?
                # For rebuild, extracting "latest state" is cleaner if we process all.
                # BUT `extract_data_regex` might return Partial info (e.g. "509 pendente" without model).
                # If we wipe the sheet, we lose the previous model if this message doesn't have it.
                # So we must maintaining a local "state cache" during processing.

                pass  # Logic implementation below

    # Processing with State Cache
    # Map local_id -> InventoryItem
    inventory_state = {}

    print("⚙️ Processing messages...")
    for msg in messages:
        body = msg["body"]
        sender = msg["sender"]
        timestamp = msg["timestamp"]

        extracted = extract_data_regex(body)
        if not extracted:
            continue

        for new_data in extracted:
            lid = new_data["local_id"]

            # Get existing or create new
            if lid in inventory_state:
                existing = inventory_state[lid]
            else:
                existing = InventoryItem(
                    local_id=lid,
                    sala=new_data.get("sala"),
                    predio=new_data.get("predio"),
                    andar=new_data.get("andar"),
                    tipo_ambiente=new_data["tipo_ambiente"],
                    status=Status.NAO_AVALIADO,
                    observacao="",
                    ultimo_responsavel=sender,
                    ultima_atualizacao=timestamp,
                )

            # Merge Logic (Manual implementation of what main.py does)

            # 1. Update Status (if not NAO_AVALIADO in new data)
            new_status_val = new_data.get("status")
            new_status = None
            if isinstance(new_status_val, str):
                new_status_val = normalize_status(new_status_val)
            if isinstance(new_status_val, Status):
                new_status = new_status_val
            elif new_status_val:  # int or other
                pass

            if new_status and new_status != Status.NAO_AVALIADO:
                existing.status = new_status

            # 2. Update Model (if present)
            if new_data.get("modelo"):
                existing.modelo = new_data["modelo"]

            # 3. Update Obs & Counts
            # Always update obs to latest? Or append?
            # Rebuild usually implies "latest status".
            existing.observacao = new_data.get("observacao", body)

            # Lab specific counts
            if new_data.get("tipo_ambiente") == TipoAmbiente.LAB:
                existing.total_pcs = new_data.get("total_pcs", existing.total_pcs)
                existing.concluidos = new_data.get("concluidos", existing.concluidos)
                existing.pendentes = new_data.get("pendentes", existing.pendentes)
                existing.erros = new_data.get("erros", existing.erros)

            # Metadata
            existing.ultimo_responsavel = sender
            existing.ultima_atualizacao = timestamp

            # Save back to state
            inventory_state[lid] = existing

    print(f"📝 Identified {len(inventory_state)} unique items.")

    # 5. Batch Upload to Sheets
    print(f"☁️ Uploading {len(inventory_state)} items to Google Sheets...")

    # Define Headers
    headers = [
        "local_id",
        "Sala",
        "Predio",
        "Andar",
        "TipoAmbiente",
        "Modelo",
        "BIOS",
        "TotalPCs",
        "Concluidos",
        "Pendentes",
        "Erros",
        "Status",
        "Observacao",
        "Setor",
        "UltimoResponsavel",
        "UltimoContato",
        "UltimaAtualizacao",
    ]

    # Prepare Data Rows
    rows = []

    # Sort locally before uploading (Predio, Andar, Sala)
    # Helper for sorting
    def get_sort_key(item):
        # Predio (int), Andar (int), Sala (str/int)
        # Handle None values safely
        p = item.predio or 0
        a = item.andar or 0
        s = item.sala or ""
        return (p, a, s)

    sorted_items = sorted(inventory_state.values(), key=get_sort_key)

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
            item.ultima_atualizacao,
        ]
        rows.append(row)

    try:
        # We already cleared A2:Z10000. Headers are assumed to be there or we should re-write them.
        # Check if we need to write headers
        # If we cleared everything including headers, we need to write them.
        # The clear command was: sheets.inventory_ws.batch_clear(["A2:Z10000"])
        # So headers at A1 should be safe.

        # Write all data at once starting A2
        if rows:
            end_row = 1 + len(rows)
            range_name = f"A2:Q{end_row}"
            sheets.inventory_ws.update(range_name=range_name, values=rows)
            print(f"✅ Successfully wrote {len(rows)} rows.")
        else:
            print("⚠️ No data to write.")

    except Exception as e:
        print(f"❌ Error during batch upload: {e}")

    print("✅ Rebuild Complete!")


if __name__ == "__main__":
    asyncio.run(rebuild_database())
