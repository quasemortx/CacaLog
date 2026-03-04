import sys
import os
import re

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.parser import extract_data_regex, Status

def test_parser_log_improvements():
    print("Testing Parser Log Improvements...")
    
    # Test 1: New Keywords (tela azul, sem espaço)
    msg1 = "615 sem espaço"
    res1 = extract_data_regex(msg1)
    print(f"Input: '{msg1}' -> Status: {res1[0]['status']}")
    assert res1[0]['status'] == Status.ERRO.value or res1[0]['status'] == Status.PENDENTE.value # Depends on mapping
    
    msg2 = "204 tela azul"
    res2 = extract_data_regex(msg2)
    print(f"Input: '{msg2}' -> Status: {res2[0]['status']}")
    assert res2[0]['status'] == Status.ERRO.value

    # Test 2: Multi-line Lab Report (from log)
    # 05/02/2026 10:53 - J.F: Lab 05 
    # 1 - win 11
    # 12 - win 10
    # (Atualizando no momento)
    
    msg_multi = """Lab 05
1 - win 11
12 - win 10
"""
    results = extract_data_regex(msg_multi)
    print(f"Input Multi-line Lab 05 -> Result: {results}")
    
    # Expect Lab 5 to capture counts from its lines
    # 1 win 11 -> Concluido: 1
    # 12 win 10 -> (win 10 logic? usually implies pendente/legacy if looking for win 11)
    # The parser logic says: `ok_match = re.search(r'(\d+)\s*(?:ok|w11|concluid[oa]s?)', ...)`
    # So "1 - win 11" should give 1 Concluido.
    
    assert results[0]['local_id'] == "L-05"
    assert results[0]['concluidos'] >= 1

    print("✅ Parser Log Tests Passed!")

if __name__ == "__main__":
    test_parser_log_improvements()
