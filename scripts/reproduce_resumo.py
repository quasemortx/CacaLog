import os
import sys

# Setup path
sys.path.append(os.getcwd())

from app.commands import handle_command


# Mock Sheets Client
class MockSheets:
    def get_all_records(self):
        return [
            # Case 1: Int
            {
                "local_id": "S-101",
                "Predio": 1,
                "TipoAmbiente": "SALA",
                "Status": "OK",
                "TotalPCs": 0,
            },
            # Case 2: Str digit
            {
                "local_id": "S-102",
                "Predio": "1",
                "TipoAmbiente": "SALA",
                "Status": "PENDENTE",
                "TotalPCs": 0,
            },
            # Case 3: "P1" (Common user entry)
            {
                "local_id": "S-103",
                "Predio": "P1",
                "TipoAmbiente": "SALA",
                "Status": "OK",
                "TotalPCs": 0,
            },
            # Case 4: Empty (Should fail)
            {
                "local_id": "S-104",
                "Predio": "",
                "TipoAmbiente": "SALA",
                "Status": "OK",
                "TotalPCs": 0,
            },
            # Case 5: Lab Inference
            {
                "local_id": "L-01",
                "Predio": "",
                "TipoAmbiente": "LAB",
                "Status": "OK",
                "TotalPCs": 10,
            },
        ]

    # Mock sheet object for /planilha command
    class Sheet:
        id = "mock_id"

    sheet = Sheet()

    def sort_inventory(self):
        pass


def test_resumo():
    # Check what the resumos give
    print("\n--- RESUMO P1 ---")
    print("Testing /resumo p1 with Mock Data...")
    sheets = MockSheets()

    # Run command
    result = handle_command("/resumo", ["p1"], sheets)
    print("\nAllowed Result:\n" + result)

    # Check validity
    if "S-103" not in result and "S-101" in result:
        print("\n[ANALYSIS] S-103 (Predio='P1') was excluded. This confirms strict digit check.")
    elif "S-103" in result:
        print("\n[ANALYSIS] S-103 (Predio='P1') was INCLUDED. Logic handles 'P1'.")
    else:
        print("\n[ANALYSIS] Unexpected result.")


if __name__ == "__main__":
    test_resumo()
