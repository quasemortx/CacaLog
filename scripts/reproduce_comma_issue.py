import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.parser import extract_data_regex


def reproduce():
    msg = "719 ,720 ,504 ,510, 511e 512 pendências com cabos resolvidos"
    print(f"Testing Input: '{msg}'")

    items = extract_data_regex(msg)

    print(f"Found {len(items)} items.")
    for i in items:
        print(f"ID: {i['local_id']} | Status: {i['status']} | Obs: {i['observacao']}")


if __name__ == "__main__":
    reproduce()
