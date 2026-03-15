from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class Local(SQLModel, table=True):
    __tablename__ = "locais"

    id: Optional[int] = Field(default=None, primary_key=True)
    local_id: str = Field(index=True, unique=True, description="S-012, L-05")
    tipo_local: str = Field(default="SALA", description="SALA or LAB")
    sala: Optional[str] = None
    predio: Optional[int] = None
    andar: Optional[int] = None
    tipo_ambiente: Optional[str] = None
    status: Optional[str] = None
    observacao: Optional[str] = None
    setor: Optional[str] = None
    
    # Infra fields
    quantidade_projetores: int = Field(default=0)
    saida_projetor: Optional[str] = None
    tomada_padrao: Optional[str] = Field(default=None, description="ANTIGO or NOVO")
    adaptador_dp_vga: int = Field(default=0)
    adaptador_dp_hdmi: int = Field(default=0)
    adaptador_hdmi_vga: int = Field(default=0)
    adaptador_duplicador_vga: int = Field(default=0)
    adaptador_outros: Optional[str] = None
    
    ultimo_responsavel: Optional[str] = None
    ultimo_contato: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    maquinas: List["Maquina"] = Relationship(back_populates="local")
    historicos: List["Historico"] = Relationship(back_populates="local")
