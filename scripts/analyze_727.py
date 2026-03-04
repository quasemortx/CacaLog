import os
import re
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.parser import extract_data_regex

LOG_FILE = "../Conversa do WhatsApp com TROPA DA T.I.txt"


def analyze_727():
    print("🔍 Searching for '727' in context of 'Chamados Manutenção'...")

    if not os.path.exists(LOG_FILE):
        print("❌ Log file not found")
        return

    with open(LOG_FILE, encoding="utf-8") as f:
        content = f.read()

    # Reconstruct messages logic (same as rebuild script)
    MSG_REGEX = re.compile(r"^(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - ([^:]+): (.*)$", re.DOTALL)

    messages = []
    current_msg = None

    lines = content.split("\n")
    for line in lines:
        match = MSG_REGEX.match(line)
        if match:
            if current_msg:
                messages.append(current_msg)
            timestamp, sender, body = match.groups()
            current_msg = {"body": body}
        else:
            if current_msg:
                current_msg["body"] += "\n" + line.strip()

    if current_msg:
        messages.append(current_msg)

    # Find the specific message
    target_msg = None
    for msg in messages:
        if "727" in msg["body"] and "Chamados Manutenção" in msg["body"]:
            target_msg = msg
            break

    if target_msg:
        print(f"\n📂 Found Message Block:\n{'-'*20}\n{target_msg['body']}\n{'-'*20}")

        print("\n⚙️ Running Parser on this block...")
        results = extract_data_regex(target_msg["body"])

        for r in results:
            print(f"\nID: {r.get('local_id')}")
            print(f"Status: {r.get('status')}")
            print(f"Obs: {r.get('observacao')}")

            if r.get("local_id") == "S-727":
                print("🚨 CHECK THIS OBSERVATION ABOVE ^")
    else:
        print("❌ Could not find the specific message.")


if __name__ == "__main__":
    analyze_727()
