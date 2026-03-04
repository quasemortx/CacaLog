import logging
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import InventoryItem, Status, TipoAmbiente
from app.sheets import SheetsClient
from app.utils import get_current_timestamp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cacalog")


def main():
    logger.info("Initializing Sheets Client...")
    sheets = SheetsClient()

    # Extracted from log message: "721\n310\n617\n619\n\n390"
    # 390 is the model context.
    manual_rooms = ["721", "310", "617", "619"]

    logger.info(f"Processing manual list: {manual_rooms}")

    all_records = sheets.get_all_records()

    for room in manual_rooms:
        # Find existing
        target_item = None
        for r in all_records:
            if str(r.get("local_id")) == str(room) or str(r.get("Sala")) == str(room):
                target_item = r
                break

        # Build Item
        if target_item:
            current_status = target_item.get("Status")
            logger.info(f"Updating Room {room} (Current: {current_status}) -> INCOMPATIVEL")

            new_item = InventoryItem(
                local_id=str(target_item.get("local_id", room)),
                sala=str(target_item.get("Sala", room)),
                predio=str(target_item.get("Predio", "1")),
                andar=str(target_item.get("Andar", "0")),
                tipo_ambiente=TipoAmbiente.SALA,
                modelo="OptiPlex 390",
                status=Status.INCOMPATIVEL,
                observacao="Lista Manual (WhatsApp)",
                ultima_atualizacao=get_current_timestamp(),
            )
            # Preserve
            if target_item.get("Predio"):
                new_item.predio = target_item.get("Predio")
            if target_item.get("Andar"):
                new_item.andar = target_item.get("Andar")
            if target_item.get("TipoAmbiente"):
                try:
                    new_item.tipo_ambiente = TipoAmbiente(target_item.get("TipoAmbiente"))
                except:
                    pass

            sheets.upsert_inventory(new_item)
        else:
            logger.info(f"Creating New Room {room} -> INCOMPATIVEL")
            new_item = InventoryItem(
                local_id=room,
                sala=room,
                predio="1",
                andar="0",
                tipo_ambiente=TipoAmbiente.SALA,
                modelo="OptiPlex 390",
                status=Status.INCOMPATIVEL,
                observacao="Lista Manual (WhatsApp)",
                ultima_atualizacao=get_current_timestamp(),
            )
            sheets.upsert_inventory(new_item)

    logger.info("Done.")


if __name__ == "__main__":
    main()
