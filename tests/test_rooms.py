from app.parser import validate_sala


def test_sala_boundaries():
    # Limite 01 e 29
    assert validate_sala("701") is not None
    assert validate_sala("729") is not None
    assert validate_sala("700") is not None  # Regra ajustada: final 00 agora é válido
    # Regra diz "entre 00 e 29". Entao 30 nao.
    assert validate_sala("730") is None


def test_predio2_boundaries():
    assert validate_sala("1001") is not None
    assert validate_sala("1029") is not None
    assert validate_sala("1030") is None
