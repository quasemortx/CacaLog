from pydantic import BaseModel
from .enums import Status, TipoAmbiente

class InventoryItem(BaseModel):
    local_id: str
    sala: str | None = None
    predio: int | None = None
    andar: int | None = None
    tipo_ambiente: TipoAmbiente
    modelo: str | None = ""
    bios: str | None = ""
    total_pcs: int = 0
    concluidos: int = 0
    pendentes: int = 0
    erros: int = 0
    status: Status
    observacao: str | None = ""
    setor_responsavel: str | None = ""
    ultimo_responsavel: str | None = ""
    ultimo_contato: str | None = ""
    ultima_atualizacao: str | None = None

class HistoryItem(BaseModel):
    timestamp: str
    local_id: str
    status: str
    observacao: str
    responsavel: str
    contato: str
    mensagem_original: str
    message_id: str
