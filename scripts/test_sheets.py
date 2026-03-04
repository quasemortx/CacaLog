import os
import sys

# Ensure app module can be found
sys.path.append(os.getcwd())

try:
    from app.sheets import SheetsClient

    print("Tentando conectar ao Google Sheets...")
    client = SheetsClient()
    print("Conexão com Google Sheets bem sucedida!")
    print(f"Planilha: {client.sheet.title}")
    print(f"Abas: {client.sheet.worksheets()}")

    # Test read
    print("Lendo primeira linha do Inventário...")
    print(client.inventory_ws.row_values(1))

except Exception as e:
    print(f"ERRO CRITICO NA CONEXÃO: {e}")
    import traceback

    traceback.print_exc()
