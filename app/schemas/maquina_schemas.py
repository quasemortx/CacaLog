from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class MaquinaBase(BaseModel):
    modelo: str
    quantidade: int = Field(default=1, ge=1)
    processador: Optional[str] = None
    propriedade: Optional[str] = Field(default="PROPRIO", description="PROPRIO, ALUGADO")
    ram_gb: Optional[int] = Field(default=None, ge=0)
    ram_modelo: Optional[str] = None
    ram_tipo: Optional[str] = None
    armazenamento_gb: Optional[int] = Field(default=None, ge=0)
    armazenamento_modelo: Optional[str] = None
    armazenamento_tipo: Optional[str] = Field(default=None, description="HDD, SSD_SATA, SSD_NVME")
    video_dp: int = Field(default=0, ge=0)
    video_hdmi: int = Field(default=0, ge=0)
    video_vga: int = Field(default=0, ge=0)

class MaquinaCreate(MaquinaBase):
    pass

class MaquinaUpdate(BaseModel):
    modelo: Optional[str] = None
    quantidade: Optional[int] = Field(default=None, ge=1)
    processador: Optional[str] = None
    propriedade: Optional[str] = None
    ram_gb: Optional[int] = Field(default=None, ge=0)
    ram_modelo: Optional[str] = None
    ram_tipo: Optional[str] = None
    armazenamento_gb: Optional[int] = Field(default=None, ge=0)
    armazenamento_modelo: Optional[str] = None
    armazenamento_tipo: Optional[str] = None
    video_dp: Optional[int] = Field(default=None, ge=0)
    video_hdmi: Optional[int] = Field(default=None, ge=0)
    video_vga: Optional[int] = Field(default=None, ge=0)

class MaquinaRead(MaquinaBase):
    id: int
    local_ref_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
