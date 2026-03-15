from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from .maquina_schemas import MaquinaRead

class LocalBase(BaseModel):
    local_id: str = Field(..., description="Ex: S-012, L-05")
    tipo_local: str = Field(..., description="SALA or LAB")
    sala: Optional[str] = None
    predio: Optional[int] = None
    andar: Optional[int] = None
    tipo_ambiente: Optional[str] = None
    status: Optional[str] = None
    observacao: Optional[str] = None
    setor: Optional[str] = None
    
    # Infra fields
    quantidade_projetores: int = Field(default=0, ge=0)
    saida_projetor: Optional[str] = None
    tomada_padrao: Optional[str] = Field(default=None, description="ANTIGO or NOVO")
    adaptador_dp_vga: int = Field(default=0, ge=0)
    adaptador_dp_hdmi: int = Field(default=0, ge=0)
    adaptador_hdmi_vga: int = Field(default=0, ge=0)
    adaptador_duplicador_vga: int = Field(default=0, ge=0)
    adaptador_outros: Optional[str] = None
    
    ultimo_responsavel: Optional[str] = None
    ultimo_contato: Optional[str] = None

class LocalCreate(LocalBase):
    pass

class LocalUpdate(BaseModel):
    tipo_local: Optional[str] = None
    sala: Optional[str] = None
    predio: Optional[int] = None
    andar: Optional[int] = None
    tipo_ambiente: Optional[str] = None
    status: Optional[str] = None
    observacao: Optional[str] = None
    setor: Optional[str] = None
    quantidade_projetores: Optional[int] = Field(default=None, ge=0)
    saida_projetor: Optional[str] = None
    tomada_padrao: Optional[str] = None
    adaptador_dp_vga: Optional[int] = Field(default=None, ge=0)
    adaptador_dp_hdmi: Optional[int] = Field(default=None, ge=0)
    adaptador_hdmi_vga: Optional[int] = Field(default=None, ge=0)
    adaptador_duplicador_vga: Optional[int] = Field(default=None, ge=0)
    adaptador_outros: Optional[str] = None
    ultimo_responsavel: Optional[str] = None
    ultimo_contato: Optional[str] = None

class LocalRead(LocalBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LocalDetailRead(BaseModel):
    local: LocalRead
    maquinas: List[MaquinaRead]
