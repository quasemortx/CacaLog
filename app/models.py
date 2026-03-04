from enum import Enum

from pydantic import BaseModel


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
    sala: str | None = None
    predio: int | None = None
    andar: int | None = None
    tipo_ambiente: TipoAmbiente
    modelo: str | None = ""
    bios: str | None = ""
    total_pcs: int = 0
    concluidos: int = 0
    pendentes: int = 0
    erros: int = 0  # New field for Lab summary
    status: Status
    observacao: str | None = ""
    setor_responsavel: str | None = ""  # TI, Manutenção, Indefinido (para não-OK)
    ultimo_responsavel: str | None = ""
    ultimo_contato: str | None = ""
    ultima_atualizacao: str | None = None  # Datetime as string for sheets


class HistoryItem(BaseModel):
    timestamp: str
    local_id: str
    status: str  # Using str to allow flexibility if raw status was logged, though mapped Status is preferred
    observacao: str
    responsavel: str
    contato: str
    mensagem_original: str
    message_id: str


class WebhookMessageData(BaseModel):
    id: str  # message id
    remoteJid: str  # sender group
    pushName: str | None = None  # Sender alias
    participant: str | None = None  # Actual sender number inside group
    conversation: str | None = None  # Text content


# Evolution API update structure may vary, simplified model for ingestion
class EvolutionWebhook(BaseModel):
    type: str  # MESSAGE_UPSERT etc
    data: dict  # Payload containing message details
