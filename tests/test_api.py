import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.db.engine import get_session
from app.models import Local, Historico
from datetime import datetime

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
client_obj = TestClient(app)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # Seed test data
        loc1 = Local(
            local_id="S-101", tipo_local="SALA", sala="101", 
            predio=1, andar=1, status="OK", setor="TI", updated_at=datetime.utcnow()
        )
        loc2 = Local(
            local_id="L-01", tipo_local="LAB", sala="Lab 1", 
            predio=1, andar=1, status="PENDENTE", setor="Manutenção", updated_at=datetime.utcnow()
        )
        session.add(loc1)
        session.add(loc2)
        
        hist = Historico(
            local_id="S-101", status="OK", responsavel="Admin", observacao="Feito"
        )
        session.add(hist)
        session.commit()
        yield session
    SQLModel.metadata.drop_all(engine)

def test_inventory_list(session):
    response = client_obj.get("/api/inventory", headers={"X-API-KEY": "dev_key"})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2

def test_inventory_filter_status(session):
    response = client_obj.get("/api/inventory?status=OK", headers={"X-API-KEY": "dev_key"})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["local_id"] == "S-101"

def test_history_list(session):
    response = client_obj.get("/api/history", headers={"X-API-KEY": "dev_key"})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1

def test_stats(session):
    response = client_obj.get("/api/stats", headers={"X-API-KEY": "dev_key"})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["by_status"]["OK"] == 1
