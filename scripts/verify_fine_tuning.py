import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.parser import extract_data_regex

def test_lab_id():
    print("Testing Lab ID standardization...")
    
    # Test 1: Lab 1
    res1 = extract_data_regex("Lab 1 OK")
    print(f"Input: 'Lab 1 OK' -> ID: {res1[0]['local_id']}")
    assert res1[0]['local_id'] == "L-01"
    
    # Test 2: Lab 12
    res2 = extract_data_regex("Lab 12 OK")
    print(f"Input: 'Lab 12 OK' -> ID: {res2[0]['local_id']}")
    assert res2[0]['local_id'] == "L-12"
    
    # Test 3: L-5
    res3 = extract_data_regex("L-5 pendente")
    print(f"Input: 'L-5 pendente' -> ID: {res3[0]['local_id']}")
    assert res3[0]['local_id'] == "L-05"

    print("✅ Lab ID tests passed!")

if __name__ == "__main__":
    test_lab_id()
