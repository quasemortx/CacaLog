import asyncio
import glob
import re

from app.parser import extract_data_regex, normalize_status
from app.sheets import SheetsClient

# Regex to parse the WhatsApp export format: dd/mm/yyyy hh:mm - Sender: Body
# Example: 26/01/2026 08:42 - J.F: 508 ✅
MSG_REGEX = re.compile(r"^(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - ([^:]+): (.*)$")


async def import_history():
    print("🚀 Starting history import...")
    client = SheetsClient()

    # Read all history files
    files = sorted(glob.glob("history*.txt"))
    if not files:
        print("❌ No history files found!")
        return

    all_lines = []
    for f in files:
        print(f"📂 Reading {f}...")
        try:
            with open(f, encoding="utf-8") as file:
                all_lines.extend(file.readlines())
        except Exception as e:
            print(f"⚠️ Error reading {f}: {e}")

    print(f"📊 Total lines to process: {len(all_lines)}")

    count_processed = 0
    count_skipped = 0

    for line in all_lines:
        line = line.strip()
        if not line:
            continue

        match = MSG_REGEX.match(line)
        if match:
            timestamp_str, sender, body = match.groups()

            # Use the exact extraction logic from parser.py (Regex fallback is faster/safer for bulk)
            # We are verifying if the regex logic correctly interprets real data
            extracted_items = extract_data_regex(body)

            if extracted_items:
                print(f"✅ Found data in: {body} -> {extracted_items}")
                for item_data in extracted_items:
                    # Update timestamp to match the message time
                    item_data["ultima_atualizacao"] = timestamp_str
                    item_data["ultimo_responsavel"] = sender

                    # Construct objects mainly for typing, though sheets.py takes objects
                    # We need to map dict back to InventoryItem if using upsert_inventory
                    # BUT `extract_data_regex` returns dicts.
                    # Let's verify models.py... InventoryItem requires specific fields.

                    from app.models import InventoryItem

                    # Handle status enum conversion if needed
                    stat = item_data["status"]
                    if isinstance(stat, str):
                        stat = normalize_status(stat)

                    inv_item = InventoryItem(
                        local_id=item_data["local_id"],
                        sala=str(item_data.get("sala") or ""),
                        predio=item_data.get("predio"),
                        andar=item_data.get("andar"),
                        tipo_ambiente=item_data["tipo_ambiente"],
                        status=stat,
                        observacao=item_data.get("observacao", body),
                        ultimo_responsavel=sender,
                        ultimo_contato=sender,  # Same as sender for history
                        ultima_atualizacao=timestamp_str,
                    )

                    # Push to sheets
                    try:
                        client.upsert_inventory(inv_item)
                        count_processed += 1
                    except Exception as e:
                        print(f"❌ Error upserting {inv_item.local_id}: {e}")
            else:
                # No relevant data found in line
                count_skipped += 1
        else:
            # Line format didn't match standard message
            count_skipped += 1

    print("🏁 Import finished!")
    print(f"✅ Processed/Updated: {count_processed}")
    print(f"⏭️ Skipped/No Data: {count_skipped}")


if __name__ == "__main__":
    asyncio.run(import_history())
