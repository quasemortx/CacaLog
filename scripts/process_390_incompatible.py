import logging
import os
import re
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import InventoryItem, Status, TipoAmbiente
from app.sheets import SheetsClient
from app.utils import get_current_timestamp

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def process_390s():
    logger.info("Initializing Sheets Client...")
    sheets = SheetsClient()

    # Files to scane
    files = [
        "history_chunk_2.txt",
        "history_chunk_3.txt",
        "history_dump.txt",  # Include dump just in case
    ]

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    found_rooms = set()

    # Regex pattern: Look for 3 digits (Room) followed by something and then 390
    # Use word boundary \b to avoid matching "2026" as "202"
    pattern = re.compile(r"\b(\d{3})\b\s*[:\-|]?\s*.*390", re.IGNORECASE)

    # Also valid table row: "| 514 | OptiPlex 390 |"
    pattern_table = re.compile(r"\|\s*(\d{3})\s*\|.*390", re.IGNORECASE)

    logger.info("Scanning history files for '390'...")

    for filename in files:
        path = os.path.join(base_dir, filename)
        if not os.path.exists(path):
            continue

        with open(path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                # Check table format first
                match_table = pattern_table.search(line)
                if match_table:
                    found_rooms.add(match_table.group(1))
                    continue

                # Check general format
                match_gen = pattern.search(line)
                if match_gen:
                    found_rooms.add(match_gen.group(1))

    logger.info(f"Found {len(found_rooms)} unique rooms with 390: {sorted(list(found_rooms))}")

    if not found_rooms:
        logger.warning("No rooms found. Exiting.")
        return

    # Bulk update would be ideal, but we'll do one by one for safety and using existing logic
    # Or we can iterate existing stats.

    # Let's fetch all records first to see what exists
    logger.info("Fetching current inventory...")
    all_records = sheets.get_all_records()

    updates_count = 0

    for room in found_rooms:
        # Check if room exists in current records to preserve other data (like Predio/Andar)
        # If not, we might need to guess (Propably Predio 1 or implicit)
        # For now, we update only matched

        # Find partial match in sheet if exact ID isn't simple (sheet uses strings)
        # We assume local_id is just the number for now based on previous interactions,
        # or we might need to construct it.
        # Let's assume input text "202" maps to local_id "202" or similar.

        target_item = None
        for r in all_records:
            if str(r.get("local_id")) == str(room) or str(r.get("Sala")) == str(room):
                target_item = r
                break

        if target_item:
            current_status = target_item.get("Status")
            # Update
            new_item = InventoryItem(
                local_id=str(target_item.get("local_id", room)),
                sala=str(target_item.get("Sala", room)),
                predio=str(target_item.get("Predio", "1")),  # Keep existing or default
                andar=str(target_item.get("Andar", "0")),  # Keep existing or default
                tipo_ambiente=TipoAmbiente.SALA,  # Default
                modelo="OptiPlex 390",
                status=Status.INCOMPATIVEL,
                observacao="Identificado via histórico (390)",
                ultima_atualizacao=get_current_timestamp(),
            )

            # Preserve existing specific fields if not null
            if target_item.get("Predio"):
                new_item.predio = target_item.get("Predio")
            if target_item.get("Andar"):
                new_item.andar = target_item.get("Andar")
            if target_item.get("TipoAmbiente"):
                try:
                    new_item.tipo_ambiente = TipoAmbiente(target_item.get("TipoAmbiente"))
                except:
                    pass

            logger.info(f"Updating Room {room}: Status {current_status} -> INCOMPATIVEL")
            sheets.upsert_inventory(new_item)
            updates_count += 1
        else:
            # New item creation (less likely if sheet is populated, but possible)
            logger.info(f"Creating New Room {room} as INCOMPATIVEL")
            new_item = InventoryItem(
                local_id=room,
                sala=room,
                predio="1",  # Default fallback
                andar="0",
                tipo_ambiente=TipoAmbiente.SALA,
                modelo="OptiPlex 390",
                status=Status.INCOMPATIVEL,
                observacao="Identificado via histórico (390)",
                ultima_atualizacao=get_current_timestamp(),
            )
            sheets.upsert_inventory(new_item)
            updates_count += 1

    logger.info(f"Finished. Total updates: {updates_count}")


if __name__ == "__main__":
    process_390s()
