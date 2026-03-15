import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.db.engine import get_session
from app.config import settings

# Setup in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

def test_crud_flow(session):
    headers = {"X-API-KEY": settings.AUTHENTICATION_API_KEY or "dev_key"}
    
    # 1. Create Local
    local_data = {
        "local_id": "TEST-01",
        "tipo_local": "LAB",
        "sala": "Test Room",
        "predio": 1,
        "andar": 2,
        "status": "OK"
    }
    response = client.post("/api/locais", json=local_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["local_id"] == "TEST-01"
    
    # 2. Add Machine
    machine_data = {
        "modelo": "Test Machine",
        "quantidade": 10,
        "processador": "i7",
        "propriedade": "PROPRIO"
    }
    response = client.post("/api/locais/TEST-01/maquinas", json=machine_data, headers=headers)
    assert response.status_code == 200
    machine_id = response.json()["id"]
    assert response.json()["modelo"] == "Test Machine"
    
    # 3. Get Detail
    response = client.get("/api/locais/TEST-01", headers=headers)
    assert response.status_code == 200
    assert len(response.json()["maquinas"]) == 1
    
    # 4. Update Machine
    update_data = {"quantidade": 15}
    response = client.put(f"/api/maquinas/{machine_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["quantidade"] == 15
    
    # 5. Delete Machine
    response = client.delete(f"/api/maquinas/{machine_id}", headers=headers)
    assert response.status_code == 204
    
    # 6. Verify Delete
    response = client.get("/api/locais/TEST-01", headers=headers)
    assert len(response.json()["maquinas"]) == 0
