from app.utils import classify_sector


def test_ti_keywords():
    assert classify_sector("ok", "precisa trocar ssd") == "TI"
    assert classify_sector("ok", "formatar a maquina") == "TI"


def test_manutencao_keywords():
    assert classify_sector("ok", "projetor sem imagem") == "Manutenção"
    assert (
        classify_sector("ok", "ar condicionado pingando") == "Manutenção"
    )  # Should default to maintenance if not IT


def test_status_based_classification():
    assert classify_sector("ok", "") == "Indefinido"
    assert classify_sector("em_manutencao", "") == "Indefinido"
