import pytest
from fastapi.testclient import TestClient

from app.main import app


class MockSheetsClient:
    def get_all_records(self):
        return [
            {
                "local_id": "S-101",
                "Sala": "101",
                "Status": "OK",
                "Setor": "TI",
                "Modelo": "Dell",
                "Observacao": "Nenhuma",
            },
            {
                "local_id": "L-01",
                "Sala": "",
                "Status": "PENDENTE",
                "Setor": "Manutenção",
                "Modelo": "",
                "Observacao": "Falta HD",
            },
        ]

    def get_all_history(self):
        return [
            {
                "local_id": "S-101",
                "status": "OK",
                "responsavel": "Admin",
                "observacao": "Feito",
                "mensagem_original": "",
            }
        ]


@pytest.fixture
def client():
    # Force mock client on app state before doing requests
    app.state.sheets_client = MockSheetsClient()
    with TestClient(app) as test_client:
        # Re-apply inside the context just in case startup_event replaced it
        app.state.sheets_client = MockSheetsClient()
        yield test_client


def test_inventory_list(client):
    response = client.get("/api/inventory")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2


def test_inventory_filter_status(client):
    response = client.get("/api/inventory?status=OK")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["local_id"] == "S-101"


def test_inventory_filter_q(client):
    response = client.get("/api/inventory?q=dell")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1


def test_history_list(client):
    response = client.get("/api/history")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1


def test_history_filter_local_id(client):
    response = client.get("/api/history?local_id=S-101")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1


def test_stats(client):
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["by_status"]["OK"] == 1
    assert "TI" in data["by_setor"]
