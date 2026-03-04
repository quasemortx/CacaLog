from app.models import Status
from app.parser import extract_data_regex, normalize_status, validate_sala


def test_validate_sala_predio_1():
    # 712 -> Predio 1, Andar 7
    res = validate_sala("712")
    assert res is not None
    assert res["predio"] == 1
    assert res["andar"] == 7
    assert res["local_id"] == "S-712"


def test_validate_sala_predio_2():
    # 4020 -> Predio 2, Andar 4
    res = validate_sala("4020")
    assert res is not None
    assert res["predio"] == 2
    assert res["andar"] == 4
    assert res["local_id"] == "S-4020"


def test_validate_sala_excecao_012():
    # 012 -> Predio 1, Andar 1
    res = validate_sala("012")
    assert res is not None
    assert res["predio"] == 1
    assert res["local_id"] == "S-012"


def test_validate_sala_invalida():
    assert validate_sala("350") is None  # Final 50 > 29
    assert validate_sala("731") is None  # Final 31 > 29


def test_extract_regex_simple():
    msg = "712 ok"
    results = extract_data_regex(msg)
    assert len(results) == 1
    assert results[0]["local_id"] == "S-712"
    assert results[0]["status"] == Status.OK


def test_extract_regex_multi_lab():
    msg = "L-03 e 21 pendentes"
    results = extract_data_regex(msg)
    # Deve achar 03 e 21
    ids = sorted([r["local_id"] for r in results])
    assert "L-03" in ids
    assert "L-21" in ids
    assert len(results) == 2
    assert results[0]["status"] == Status.PENDENTE


def test_extract_regex_lab_only_digits():
    msg = "05 erro"
    results = extract_data_regex(msg)
    assert len(results) == 1
    assert results[0]["local_id"] == "L-05"
    assert results[0]["status"] == Status.ERRO


def test_normalize_status():
    assert normalize_status("feito") == Status.OK
    assert normalize_status("sem ssd") == Status.PENDENTE
