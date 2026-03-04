import sys
import os
import logging

# Add parent directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.sheets import SheetsClient
from app.logging_conf import configure_logging

# Configure logging to see output
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cacalog")

def main():
    print("Initializing Sheets Client...")
    try:
        sheets = SheetsClient()
        print("Connected. Attempting to sort...")
        sheets._sort_inventory()
        print("Sort function execution completed. Check formatting.")
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    main()
