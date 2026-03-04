import sys
import os
sys.path.append(os.getcwd())
from app.sheets import SheetsClient
from app.config import settings

print("Testing Sheets Client...")
try:
    s = SheetsClient()
    print(f"Sheet Object: {s.sheet}")
    print(f"Sheet ID: {s.sheet.id}")
    has_attr = hasattr(s, 'sheet')
    print(f"Has 'sheet' attr: {has_attr}")
    url = f"https://docs.google.com/spreadsheets/d/{s.sheet.id}"
    print(f"Generated URL: {url}")
except Exception as e:
    print(f"Error: {e}")
