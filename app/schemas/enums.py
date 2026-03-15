from enum import StrEnum
from pydantic import BaseModel

class Status(StrEnum):
    OK = "OK"
    PENDENTE = "PENDENTE"
    ERRO = "ERRO"
    INCOMPATIVEL = "INCOMPATIVEL"
    NAO_AVALIADO = "NAO_AVALIADO"
    ATUALIZANDO = "ATUALIZANDO"

class TipoAmbiente(StrEnum):
    SALA = "SALA"
    LAB = "LAB"

class WebhookMessageData(BaseModel):
    id: str  
    remoteJid: str  
    pushName: str | None = None  
    participant: str | None = None  
    conversation: str | None = None  

class EvolutionWebhook(BaseModel):
    type: str  
    data: dict  
