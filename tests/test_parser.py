from app.parser import extract_data_regex


def test_parse_room():
    items = extract_data_regex("S-712 ok")
    assert len(items) == 1
    assert items[0]["local_id"] == "S-712"
    assert items[0]["sala"] == "712"
    assert items[0]["tipo_ambiente"] == "SALA"


def test_parse_lab():
    items = extract_data_regex("L-03 pendente")
    assert len(items) == 1
    assert items[0]["local_id"] == "L-03"
    assert items[0]["tipo_ambiente"] == "LABORATORIO"
