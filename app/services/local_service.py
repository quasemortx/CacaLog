from typing import List, Optional
from sqlmodel import Session
from datetime import datetime
from app.models.local import Local
from app.models.maquina import Maquina
from app.models.historico import Historico
from app.repositories.local_repository import LocalRepository
from app.repositories.maquina_repository import MaquinaRepository
from app.schemas.local_schemas import LocalCreate, LocalUpdate
from app.schemas.maquina_schemas import MaquinaCreate, MaquinaUpdate

class LocalService:
    def __init__(self, session: Session):
        self.session = session
        self.local_repo = LocalRepository(session)
        self.maquina_repo = MaquinaRepository(session)

    def create_local(self, data: LocalCreate) -> Local:
        existing = self.local_repo.get_by_local_id(data.local_id)
        if existing:
            raise ValueError(f"Local with ID {data.local_id} already exists")
        
        local = Local(**data.model_dump())
        local.created_at = datetime.utcnow()
        local.updated_at = datetime.utcnow()
        
        created = self.local_repo.create(local)
        
        self._add_history(
            local_ref_id=created.id,
            local_id=created.local_id,
            status=created.status,
            observacao="Local criado via painel/API"
        )
        
        return created

    def get_local_detail(self, local_id: str) -> dict:
        local = self.local_repo.get_by_local_id(local_id)
        if not local:
            return None
        
        maquinas = self.maquina_repo.get_by_local_id(local.id)
        return {
            "local": local,
            "maquinas": maquinas
        }

    def update_local(self, local_id: str, data: LocalUpdate) -> Local:
        local = self.local_repo.get_by_local_id(local_id)
        if not local:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(local, key, value)
        
        local.updated_at = datetime.utcnow()
        updated = self.local_repo.update(local)
        
        self._add_history(
            local_ref_id=updated.id,
            local_id=updated.local_id,
            status=updated.status,
            observacao="Local atualizado via painel/API"
        )
        
        return updated

    def add_maquina(self, local_id: str, data: MaquinaCreate) -> Maquina:
        local = self.local_repo.get_by_local_id(local_id)
        if not local:
            return None
        
        maquina = Maquina(**data.model_dump())
        maquina.local_ref_id = local.id
        maquina.created_at = datetime.utcnow()
        maquina.updated_at = datetime.utcnow()
        
        created = self.maquina_repo.create(maquina)
        
        self._add_history(
            local_ref_id=local.id,
            local_id=local.local_id,
            observacao=f"Máquina ({created.modelo}) adicionada ao local"
        )
        
        return created

    def update_maquina(self, maquina_id: int, data: MaquinaUpdate) -> Maquina:
        maquina = self.maquina_repo.get_by_id(maquina_id)
        if not maquina:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(maquina, key, value)
        
        maquina.updated_at = datetime.utcnow()
        updated = self.maquina_repo.update(maquina)
        
        local = self.local_repo.get_by_id(updated.local_ref_id)
        self._add_history(
            local_ref_id=local.id if local else None,
            local_id=local.local_id if local else None,
            observacao=f"Máquina ({updated.modelo}) atualizada"
        )
        
        return updated

    def delete_maquina(self, maquina_id: int) -> bool:
        maquina = self.maquina_repo.get_by_id(maquina_id)
        if not maquina:
            return False
        
        local = self.local_repo.get_by_id(maquina.local_ref_id)
        modelo = maquina.modelo
        
        self.maquina_repo.delete(maquina)
        
        if local:
            self._add_history(
                local_ref_id=local.id,
                local_id=local.local_id,
                observacao=f"Máquina ({modelo}) removida"
            )
        
        return True

    def _add_history(self, local_ref_id: Optional[int], local_id: Optional[str], status: Optional[str] = None, observacao: str = ""):
        history = Historico(
            local_ref_id=local_ref_id,
            local_id=local_id,
            status=status,
            observacao=observacao,
            responsavel="API",
            created_at=datetime.utcnow()
        )
        self.session.add(history)
        self.session.commit()
