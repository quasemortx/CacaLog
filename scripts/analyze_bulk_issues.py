import os
import re
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.parser import extract_data_regex

LOG_FILE = "../Conversa do WhatsApp com TROPA DA T.I.txt"

TARGET_IDS = [
    "S-726",
    "S-720",
    "S-713",
    "S-711",
    "S-510",
    "S-511",
    "S-512",
    "S-504",
    "L-07",
    "L-01",
    "L-03",
    "L-02",
]


def analyze_bulk_issues():
    print(f"🔍 Searching for issues with: {TARGET_IDS}")

    if not os.path.exists(LOG_FILE):
        print("❌ Log file not found")
        return

    with open(LOG_FILE, encoding="utf-8") as f:
        content = f.read()

    # Reconstruct messages logic
    MSG_REGEX = re.compile(r"^(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - ([^:]+): (.*)$", re.DOTALL)

    messages = []
    current_msg = None

    lines = content.split("\n")
    for line in lines:
        match = MSG_REGEX.match(line)
        if match:
            if current_msg:
                messages.append(current_msg)
            _timestamp, _sender, body = match.groups()
            current_msg = {"body": body}
        else:
            if current_msg:
                current_msg["body"] += "\n" + line.strip()

    if current_msg:
        messages.append(current_msg)

    # Process all messages and check if Targets have "bad" observations
    # A "bad" observation typically handles newlines or refers to other IDs.


    print("\n---------------- RESULTS ----------------")

    for msg in messages:
        # Optimization: Only parse if message contains one of the target raw numbers
        # to speed up testing
        body_lower = msg["body"].lower()

        # Check if relevant
        is_relevant = False
        for tid in TARGET_IDS:
            # Check for "726" or "07"
            num = tid.split("-")[1]
            if num in body_lower:  # simple check
                is_relevant = True
                break

        if not is_relevant:
            continue

        results = extract_data_regex(msg["body"])

        for r in results:
            if r.get("local_id") in TARGET_IDS:
                obs = r.get("observacao", "")
                # simplistic check for "bleed": if obs has multiple lines and mentions OTHER IDs
                if "\n" in obs:  # Multi-line observation suggests full message capture
                    print(f"\n[!] Potentially Bad Observation for {r.get('local_id')}:")
                    print(f"    Obs Length: {len(obs)}")
                    print(f"    Content Preview: {obs[:100]}...")
                    if len(obs) > 200:
                        print("    -> LIKELY FULL MESSAGE BLEED")
                        # Print full for debugging
                        # print(f"    FULL: {obs}")

    print("\n---------------- END ----------------")


if __name__ == "__main__":
    analyze_bulk_issues()
