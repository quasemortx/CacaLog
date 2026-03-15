from typing import List, Optional
from sqlmodel import Session, select
from app.models.maquina import Maquina

class MaquinaRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> Optional[Maquina]:
        return self.session.get(Maquina, id)

    def get_by_local_id(self, local_ref_id: int) -> List[Maquina]:
        statement = select(Maquina).where(Maquina.local_ref_id == local_ref_id)
        return self.session.exec(statement).all()

    def create(self, maquina: Maquina) -> Maquina:
        self.session.add(maquina)
        self.session.commit()
        self.session.refresh(maquina)
        return maquina

    def update(self, maquina: Maquina) -> Maquina:
        self.session.add(maquina)
        self.session.commit()
        self.session.refresh(maquina)
        return maquina

    def delete(self, maquina: Maquina) -> None:
        self.session.delete(maquina)
        self.session.commit()
