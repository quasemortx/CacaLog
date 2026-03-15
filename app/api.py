from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session

from app.security import require_api_key
from app.db.engine import get_session
from app.services.inventory_service import InventoryService
from app.services.history_service import HistoryService
from app.services.stats_service import StatsService
from app.services.local_service import LocalService
from app.schemas.inventory import InventoryListResponse
from app.schemas.history import HistoryListResponse
from app.schemas.stats import StatsResponse
from app.schemas.local_schemas import LocalCreate, LocalRead, LocalUpdate, LocalDetailRead
from app.schemas.maquina_schemas import MaquinaCreate, MaquinaRead, MaquinaUpdate

router = APIRouter(prefix="/api", dependencies=[Depends(require_api_key)])

@router.get("/inventory", response_model=InventoryListResponse)
def list_inventory(
    q: str | None = None, 
    status: str | None = None, 
    setor: str | None = None,
    session: Session = Depends(get_session)
):
    service = InventoryService(session)
    items, total = service.get_inventory(query=q, status=status, setor=setor)
    return InventoryListResponse(items=items, total=total)


@router.get("/history", response_model=HistoryListResponse)
def list_history(
    q: str | None = None, 
    local_id: str | None = None,
    session: Session = Depends(get_session)
):
    service = HistoryService(session)
    items, total = service.get_history(query=q, local_id=local_id)
    return HistoryListResponse(items=items, total=total)


@router.get("/stats", response_model=StatsResponse)
def get_stats(session: Session = Depends(get_session)):
    service = StatsService(session)
    return service.get_stats()

# Locais CRUD
@router.post("/locais", response_model=LocalRead)
def create_local(data: LocalCreate, session: Session = Depends(get_session)):
    service = LocalService(session)
    try:
        return service.create_local(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/locais/{local_id}", response_model=LocalDetailRead)
def get_local_detail(local_id: str, session: Session = Depends(get_session)):
    service = LocalService(session)
    detail = service.get_local_detail(local_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Local not found")
    return detail

@router.put("/locais/{local_id}", response_model=LocalRead)
def update_local(local_id: str, data: LocalUpdate, session: Session = Depends(get_session)):
    service = LocalService(session)
    updated = service.update_local(local_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Local not found")
    return updated

# Máquinas CRUD
@router.post("/locais/{local_id}/maquinas", response_model=MaquinaRead)
def add_maquina(local_id: str, data: MaquinaCreate, session: Session = Depends(get_session)):
    service = LocalService(session)
    created = service.add_maquina(local_id, data)
    if not created:
        raise HTTPException(status_code=404, detail="Local not found")
    return created

@router.put("/maquinas/{maquina_id}", response_model=MaquinaRead)
def update_maquina(maquina_id: int, data: MaquinaUpdate, session: Session = Depends(get_session)):
    service = LocalService(session)
    updated = service.update_maquina(maquina_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Machine not found")
    return updated

@router.delete("/maquinas/{maquina_id}", status_code=204)
def delete_maquina(maquina_id: int, session: Session = Depends(get_session)):
    service = LocalService(session)
    if not service.delete_maquina(maquina_id):
        raise HTTPException(status_code=404, detail="Machine not found")
    return None
