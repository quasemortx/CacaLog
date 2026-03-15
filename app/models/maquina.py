from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class Maquina(SQLModel, table=True):
    __tablename__ = "maquinas"

    id: Optional[int] = Field(default=None, primary_key=True)
    local_ref_id: int = Field(foreign_key="locais.id", index=True)
    modelo: str
    quantidade: int = Field(default=1)
    
    # Specs
    processador: Optional[str] = None
    propriedade: Optional[str] = Field(default=None, description="PROPRIO, ALUGADO")
    ram_gb: Optional[int] = None
    ram_modelo: Optional[str] = None
    ram_tipo: Optional[str] = None
    armazenamento_gb: Optional[int] = None
    armazenamento_modelo: Optional[str] = None
    armazenamento_tipo: Optional[str] = Field(default=None, description="HDD, SSD_SATA, SSD_NVME")
    
    # Adapters/Video inside machine
    video_dp: int = Field(default=0)
    video_hdmi: int = Field(default=0)
    video_vga: int = Field(default=0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    local: "Local" = Relationship(back_populates="maquinas")
