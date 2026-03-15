from sqlmodel import Session, select
from app.models import Local
from app.schemas.stats import StatsResponse

class StatsService:
    def __init__(self, session: Session):
        self.session = session
        
    def get_stats(self) -> StatsResponse:
        statement = select(Local)
        locais = self.session.exec(statement).all()
        
        by_status = {}
        by_setor = {}
        
        for loc in locais:
            st = loc.status or "NÃO AVALIADO"
            st = st.replace("_", " ") # standardize as before
            by_status[st] = by_status.get(st, 0) + 1
            
            setor_val = loc.setor or "Sem Setor"
            by_setor[setor_val] = by_setor.get(setor_val, 0) + 1
            
        return StatsResponse(
            total=len(locais),
            by_status=by_status,
            by_setor=by_setor
        )
