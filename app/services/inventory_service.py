from sqlmodel import Session, select
from app.models import Local, Maquina
from app.schemas.inventory import FrontendInventoryItem

class InventoryService:
    def __init__(self, session: Session):
        self.session = session
        
    def get_inventory(self, query: str = None, status: str = None, setor: str = None) -> tuple[list[FrontendInventoryItem], int]:
        statement = select(Local, Maquina).outerjoin(Maquina)
        results = self.session.exec(statement).all()
        
        # Aggregate logic
        local_map = {}
        
        for local, maquina in results:
            if local.id not in local_map:
                local_map[local.id] = {
                    "local": local,
                    "modelos": [],
                    "total_pcs": 0
                }
            if maquina:
                local_map[local.id]["modelos"].append(maquina.modelo)
                local_map[local.id]["total_pcs"] += maquina.quantidade
                
        items = []
        for l_id, data in local_map.items():
            loc: Local = data["local"]
            modelos = data["modelos"]
            
            # Use the first model or empty
            first_modelo = modelos[0] if modelos else None
            
            # Simple check for Concluidos / Pendentes
            # If status == OK, concluidos = total_pcs
            # If status == PENDENTE or ERRO, pendentes = total_pcs (naive logic for now)
            total = data["total_pcs"]
            concluidos = total if loc.status == "OK" else 0
            erros = total if loc.status == "ERRO" else 0
            pendentes = total - concluidos - erros
            
            item = FrontendInventoryItem(
                local_id=loc.local_id,
                Sala=loc.sala,
                Predio=loc.predio,
                Andar=loc.andar,
                TipoAmbiente=loc.tipo_ambiente,
                Modelo=first_modelo,
                BIOS=None,
                TotalPCs=total,
                Concluidos=concluidos,
                Pendentes=pendentes,
                Erros=erros,
                Status=loc.status or "NAO AVALIADO",
                Observacao=loc.observacao or "",
                Setor=loc.setor or "INDEFINIDO",
                UltimoResponsavel=loc.ultimo_responsavel or "",
                UltimoContato=loc.ultimo_contato or "",
                UltimaAtualizacao=loc.updated_at.isoformat() if loc.updated_at else None
            )
            items.append(item)
            
        # Filter in python to reuse same search logic for now
        filtered = []
        for item in items:
            if query:
                searchable = f"{item.local_id or ''} {item.Sala or ''} {item.Modelo or ''} {item.Observacao or ''} {item.Setor or ''}".lower()
                if query.lower() not in searchable:
                    continue
            if status and (item.Status or "").lower() != status.lower():
                continue
            if setor and (item.Setor or "").lower() != setor.lower():
                continue
                
            filtered.append(item)
            
        return filtered, len(filtered)
