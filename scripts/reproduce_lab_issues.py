import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.parser import extract_data_regex


def reproduce_issues():
    print("🚀 Starting Reproduction Tests...")

    # Test Case 1: Lab Pipe Splitting (Regression Check)
    msg1 = (
        "lab 2 - 37 máquinas apenas 1 w11 | lab 1 - 14 máquinas apenas 11 w11 | lab 3 - 19 máquinas"
    )
    print(f"\n--- Test 1: Lab Pipe Splitting ---\nInput: '{msg1}'")
    items1 = extract_data_regex(msg1)

    l1 = next((i for i in items1 if i["local_id"] == "L-01"), None)
    if l1:
        print(f"L-01 Obs: {l1['observacao']}")
        if "lab 2" in l1["observacao"]:
            print("❌ BLEED: L-01 contains Lab 2")
        else:
            print("✅ L-01 Clean")

    # Test Case 2: Lab Pendentes Inference
    msg2 = "lab 5 - 13 máquinas apenas 1 w11"
    print(f"\n--- Test 2: Lab Pendentes Inference ---\nInput: '{msg2}'")
    items2 = extract_data_regex(msg2)
    l5 = next((i for i in items2 if i["local_id"] == "L-05"), None)
    if l5:
        print(f"L-05: Total={l5['total_pcs']}, OK={l5['concluidos']}, Pend={l5['pendentes']}")
        if l5["pendentes"] == 12:
            print("✅ Pendentes Correct (12)")
        else:
            print(f"❌ Pendentes Incorrect (Got {l5['pendentes']})")

    # Test Case 3: Room Pipe Splitting
    msg3 = "Chamados Manutenção: | S-313: PENDENTE (Sala 313 pendente) | S-504: PENDENTE (504 cabo)"
    print(f"\n--- Test 3: Room Pipe Splitting ---\nInput: '{msg3}'")
    items3 = extract_data_regex(msg3)

    s313 = next((i for i in items3 if i["local_id"] == "S-313"), None)
    s504 = next((i for i in items3 if i["local_id"] == "S-504"), None)

    if s313:
        print(f"S-313 Obs: {s313['observacao']}")
        if "504" in s313["observacao"]:
            print("❌ BLEED: S-313 contains S-504")
        else:
            print("✅ S-313 Clean")

    if s504:
        print(f"S-504 Obs: {s504['observacao']}")
        if "313" in s504["observacao"]:
            print("❌ BLEED: S-504 contains S-313")
        else:
            print("✅ S-504 Clean")

    # Test Case 4: L-1 Check
    msg4 = "Lab 1 - teste"
    print(f"\n--- Test 4: L-1 ID Generation ---\nInput: '{msg4}'")
    items4 = extract_data_regex(msg4)
    l1_chk = next((i for i in items4 if "L-" in i["local_id"]), None)
    if l1_chk:
        print(f"Generated ID: {l1_chk['local_id']}")
        if l1_chk["local_id"] == "L-01":
            print("✅ Correct Format (L-01)")
        else:
            print(f"❌ Bad Format ({l1_chk['local_id']})")


if __name__ == "__main__":
    reproduce_issues()
