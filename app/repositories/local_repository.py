from typing import List, Optional
from sqlmodel import Session, select
from app.models.local import Local

class LocalRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> Optional[Local]:
        return self.session.get(Local, id)

    def get_by_local_id(self, local_id: str) -> Optional[Local]:
        statement = select(Local).where(Local.local_id == local_id)
        return self.session.exec(statement).first()

    def create(self, local: Local) -> Local:
        self.session.add(local)
        self.session.commit()
        self.session.refresh(local)
        return local

    def update(self, local: Local) -> Local:
        self.session.add(local)
        self.session.commit()
        self.session.refresh(local)
        return local

    def delete(self, local: Local) -> None:
        self.session.delete(local)
        self.session.commit()
