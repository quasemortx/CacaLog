from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session

from app.security import require_api_key
from app.db.engine import get_session
from app.services.inventory_service import InventoryService
from app.services.history_service import HistoryService
from app.services.stats_service import StatsService
from app.schemas.inventory import InventoryListResponse
from app.schemas.history import HistoryListResponse
from app.schemas.stats import StatsResponse

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
