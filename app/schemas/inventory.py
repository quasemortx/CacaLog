from typing import List, Optional, Union
from pydantic import BaseModel

class FrontendInventoryItem(BaseModel):
    local_id: str
    Sala: Optional[str] = None
    Predio: Optional[Union[str, int]] = None
    Andar: Optional[Union[str, int]] = None
    TipoAmbiente: Optional[str] = None
    Modelo: Optional[str] = None
    BIOS: Optional[str] = None
    TotalPCs: Optional[Union[str, int]] = 0
    Concluidos: Optional[Union[str, int]] = 0
    Pendentes: Optional[Union[str, int]] = 0
    Erros: Optional[Union[str, int]] = 0
    Status: str
    Observacao: Optional[str] = None
    Setor: Optional[str] = None
    UltimoResponsavel: Optional[str] = None
    UltimoContato: Optional[str] = None
    UltimaAtualizacao: Optional[str] = None

class InventoryListResponse(BaseModel):
    items: List[FrontendInventoryItem]
    total: int
