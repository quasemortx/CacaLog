from sqlmodel import Session, select
from app.models import Historico
from app.schemas.history import FrontendHistoryItem

class HistoryService:
    def __init__(self, session: Session):
        self.session = session
        
    def get_history(self, query: str = None, local_id: str = None) -> tuple[list[FrontendHistoryItem], int]:
        statement = select(Historico).order_by(Historico.created_at.desc())
        
        db_items = self.session.exec(statement).all()
        
        items = []
        for h in db_items:
            item = FrontendHistoryItem(
                timestamp=h.created_at.isoformat(),
                local_id=h.local_id or "GERAL",
                status=h.status or "EVENTO",
                observacao=h.observacao or "",
                responsavel=h.responsavel or "Sistema",
                contato=h.contato or "",
                mensagem_original=h.mensagem_original,
                message_id=h.message_id
            )
            items.append(item)
            
        filtered = []
        for item in items:
            if query:
                searchable = f"{item.local_id or ''} {item.observacao or ''} {item.responsavel or ''} {item.mensagem_original or ''}".lower()
                if query.lower() not in searchable:
                    continue
            if local_id and (item.local_id or "").lower() != local_id.lower():
                continue
            filtered.append(item)
            
        return filtered, len(filtered)
