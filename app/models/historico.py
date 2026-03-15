from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class Historico(SQLModel, table=True):
    __tablename__ = "historicos"

    id: Optional[int] = Field(default=None, primary_key=True)
    local_ref_id: Optional[int] = Field(default=None, foreign_key="locais.id")
    local_id: Optional[str] = Field(default=None, index=True)
    status: Optional[str] = None
    observacao: Optional[str] = None
    responsavel: Optional[str] = None
    contato: Optional[str] = None
    mensagem_original: Optional[str] = None
    message_id: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    
    local: Optional["Local"] = Relationship(back_populates="historicos")
