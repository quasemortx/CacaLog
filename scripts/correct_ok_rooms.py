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

    # "310 \n202\n617\n619 \nOk" -> These are NO LONGER 390.
    correction_rooms = ["310", "202", "617", "619"]

    logger.info(f"Applying corrections (OK + Remove Model 390) for: {correction_rooms}")

    all_records = sheets.get_all_records()

    for room in correction_rooms:
        target_item = None
        for r in all_records:
            if str(r.get("local_id")) == str(room) or str(r.get("Sala")) == str(room):
                target_item = r
                break

        if target_item:
            current_status = target_item.get("Status")
            current_model = target_item.get("Modelo")
            logger.info(
                f"Correcting Room {room} (Status: {current_status}, Model: {current_model}) -> OK / Model Cleared"
            )

            # Create update item
            new_item = InventoryItem(
                local_id=str(target_item.get("local_id", room)),
                sala=str(target_item.get("Sala", room)),
                predio=str(target_item.get("Predio", "1")),
                andar=str(target_item.get("Andar", "0")),
                tipo_ambiente=TipoAmbiente.SALA,
                modelo="",  # Clear model as requested ("deixaram de ser 390")
                status=Status.OK,  # OK logic
                observacao="Correção Manual (Ok - Não é 390)",
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
            logger.warning(f"Room {room} not found in sheet to correct. Creating compliant entry.")
            new_item = InventoryItem(
                local_id=room,
                sala=room,
                predio="1",
                andar="0",
                tipo_ambiente=TipoAmbiente.SALA,
                modelo="",
                status=Status.CONCLUIDO,
                observacao="Correção Manual (Ok - Não é 390)",
                ultima_atualizacao=get_current_timestamp(),
            )
            sheets.upsert_inventory(new_item)

    logger.info("Correction complete.")


if __name__ == "__main__":
    main()
