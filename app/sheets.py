import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app.config import settings
from app.models import InventoryItem, HistoryItem
from app.logging_conf import logger
from typing import Optional, List, Dict

SCOPES = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
          "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

class SheetsClient:
    def __init__(self):
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            settings.GOOGLE_SERVICE_ACCOUNT_JSON_PATH, SCOPES
        )
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open_by_key(settings.GOOGLE_SHEETS_ID)
        
        try:
            self.inventory_ws = self.sheet.worksheet(settings.GOOGLE_WORKSHEET_INVENTARIO)
        except gspread.exceptions.WorksheetNotFound:
            self.inventory_ws = self.sheet.add_worksheet(title=settings.GOOGLE_WORKSHEET_INVENTARIO, rows=1000, cols=20)
            
        try:
            self.history_ws = self.sheet.worksheet(settings.GOOGLE_WORKSHEET_HISTORICO)
        except gspread.exceptions.WorksheetNotFound:
            self.history_ws = self.sheet.add_worksheet(title=settings.GOOGLE_WORKSHEET_HISTORICO, rows=1000, cols=20)
            
        self._ensure_headers()

    def _ensure_headers(self):
        # Basic headers check, could be expanded
        # Added Erros at index 10 (Column 11), shifting others.
        inv_headers = ["local_id", "Sala", "Predio", "Andar", "TipoAmbiente", "Modelo", "BIOS", "TotalPCs", "Concluidos", "Pendentes", "Erros", "Status", "Observacao", "Setor", "UltimoResponsavel", "UltimoContato", "UltimaAtualizacao"]
        hist_headers = ["timestamp", "local_id", "status", "observacao", "responsavel", "contato", "mensagem_original", "message_id"]
        
        current_inv = self.inventory_ws.row_values(1)
        if not current_inv:
            self.inventory_ws.append_row(inv_headers)
        elif "Erros" not in current_inv:
            # Migration needed logic handled by script usually
            pass

    # ...

    def upsert_inventory(self, item: InventoryItem):
        try:
            cell = self.inventory_ws.find(item.local_id, in_column=1)
            row_data = [
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
                item.erros, # New Col
                item.status.value,
                item.observacao,
                item.setor_responsavel,
                item.ultimo_responsavel,
                item.ultimo_contato,
                item.ultima_atualizacao
            ]
            
            if cell:
                # Update existing
                # Range updated to Q (17 cols)
                cell_range = f"A{cell.row}:Q{cell.row}" 
                self.inventory_ws.update(range_name=cell_range, values=[row_data])
            else:
                # Insert new
                self.inventory_ws.append_row(row_data)
            
            # Organize: Sort by Predio (3), Andar (4), Sala (2)
            # Organize: Sort by Predio (3), Andar (4), Sala (2)
            self.sort_inventory()
            
        except Exception as e:
            logger.error(f"Error upserting inventory: {e}")
            raise e

    def sort_inventory(self):
        try:
            # Sort by Predio (3), Andar (4), Sala (2)
            # Range A2:O to skip header
            self.inventory_ws.sort((3, 'asc'), (4, 'asc'), (2, 'asc'), range='A2:O1000')
        except Exception as e:
            logger.warning(f"Sorting failed (api limit or other): {e}")

    def add_history(self, item: HistoryItem):
        try:
            row_data = [
                item.timestamp,
                item.local_id,
                item.status,
                item.observacao,
                item.responsavel,
                item.contato,
                item.mensagem_original,
                item.message_id
            ]
            self.history_ws.append_row(row_data)
        except Exception as e:
            logger.error(f"Error adding history: {e}")
            raise e
            
    def get_all_records(self):
        return self.inventory_ws.get_all_records()

    def get_all_history(self) -> List[Dict]:
        return self.history_ws.get_all_records()

    def delete_inventory_item(self, local_id: str) -> bool:
        """Remove a row from the inventory worksheet by local_id.
        Returns True if found and deleted, False if not found.
        """
        try:
            cell = self.inventory_ws.find(local_id, in_column=1)
            if not cell:
                return False
            self.inventory_ws.delete_rows(cell.row)
            logger.info(f"Deleted inventory row for {local_id} (row {cell.row})")
            return True
        except Exception as e:
            logger.error(f"Error deleting item {local_id}: {e}")
            raise e

    def get_inventory_item(self, local_id: str) -> Optional[Dict]:
        """
        Fetches a single item by local_id.
        Returns Dict or None if not found.
        """
        try:
            cell = self.inventory_ws.find(local_id, in_column=1)
            if cell:
                # Get all values for the row
                row_values = self.inventory_ws.row_values(cell.row)
                headers = self.inventory_ws.row_values(1)
                
                # Create dict manually or use get_all_records approach (slower)
                # Ensure row_values has enough columns (pad with empty strings)
                if len(row_values) < len(headers):
                    row_values += [""] * (len(headers) - len(row_values))
                
                return dict(zip(headers, row_values))
            return None
        except Exception as e:
            logger.error(f"Error fetching item {local_id}: {e}")
            return None

# Singleton-ish access could be done here or in dependency injection
# For simplicity, creating when needed or global if thread-safe enough for gspread (usually is per request)
