from typing import List, Optional
from pydantic import BaseModel

class FrontendHistoryItem(BaseModel):
    timestamp: str
    local_id: str
    status: str
    observacao: str
    responsavel: str
    contato: str
    mensagem_original: Optional[str] = None
    message_id: Optional[str] = None

class HistoryListResponse(BaseModel):
    items: List[FrontendHistoryItem]
    total: int
