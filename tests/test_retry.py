import pytest

from app.retry import retry_sync


def test_retry_sync_success_first_try():
    calls = 0

    def mock_func():
        nonlocal calls
        calls += 1
        return "success"

    result = retry_sync(mock_func)
    assert result == "success"
    assert calls == 1


def test_retry_sync_success_after_retries():
    calls = 0

    def mock_func():
        nonlocal calls
        calls += 1
        if calls < 3:
            raise ValueError("Falha temporaria")
        return "success"

    result = retry_sync(mock_func)
    assert result == "success"
    assert calls == 3


def test_retry_sync_failure():
    calls = 0

    def mock_func():
        nonlocal calls
        calls += 1
        raise ValueError("Falha permanente")

    with pytest.raises(ValueError, match="Falha permanente"):
        retry_sync(mock_func, tries=3, base_delay=0.1)

    assert calls == 3
