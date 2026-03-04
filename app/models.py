from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class Status(str, Enum):
    OK = "OK"
    PENDENTE = "PENDENTE"
    ERRO = "ERRO"
    INCOMPATIVEL = "INCOMPATIVEL"
    NAO_AVALIADO = "NAO_AVALIADO"
    ATUALIZANDO = "ATUALIZANDO"

class TipoAmbiente(str, Enum):
    SALA = "SALA"
    LAB = "LAB"

class InventoryItem(BaseModel):
    local_id: str  # PK: S-712, L-03
    sala: Optional[str] = None
    predio: Optional[int] = None
    andar: Optional[int] = None
    tipo_ambiente: TipoAmbiente
    modelo: Optional[str] = ""
    bios: Optional[str] = ""
    total_pcs: int = 0
    concluidos: int = 0
    pendentes: int = 0
    erros: int = 0 # New field for Lab summary
    status: Status
    observacao: Optional[str] = ""
    setor_responsavel: Optional[str] = "" # TI, Manutenção, Indefinido (para não-OK)
    ultimo_responsavel: Optional[str] = ""
    ultimo_contato: Optional[str] = ""
    ultima_atualizacao: Optional[str] = None # Datetime as string for sheets

class HistoryItem(BaseModel):
    timestamp: str 
    local_id: str
    status: str # Using str to allow flexibility if raw status was logged, though mapped Status is preferred
    observacao: str
    responsavel: str
    contato: str
    mensagem_original: str
    message_id: str

class WebhookMessageData(BaseModel):
    id: str # message id
    remoteJid: str # sender group
    pushName: Optional[str] = None # Sender alias
    participant: Optional[str] = None # Actual sender number inside group
    conversation: Optional[str] = None # Text content

# Evolution API update structure may vary, simplified model for ingestion
class EvolutionWebhook(BaseModel):
    type: str # MESSAGE_UPSERT etc
    data: dict # Payload containing message details
