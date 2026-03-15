from sqlmodel import Session, select
from app.db.engine import engine
from app.models import Local, Maquina, Historico
import logging

logger = logging.getLogger(__name__)

def init_db():
    with Session(engine) as session:
        # Check if already seeded
        local_exists = session.exec(select(Local).first()).first()
        if local_exists:
            logger.info("Database already seeded.")
            print("Database already seeded.")
            return
            
        # 1 Sala
        sala = Local(
            local_id="S-101", tipo_local="SALA", sala="Sala de Aula 101", 
            predio=1, andar=1, tipo_ambiente="SALA", status="OK", observacao="Sala funcionando perfeitamente.",
            setor="TI", ultimo_responsavel="Filipe", ultimo_contato="551199999999"
        )
        
        # 1 Lab
        lab = Local(
            local_id="L-01", tipo_local="LAB", sala="Laboratório de Informática 01",
            predio=2, andar=1, tipo_ambiente="LAB", status="PENDENTE", observacao="Faltando switch para algums computadores.",
            setor="TI", ultimo_responsavel="Filipe"
        )
        
        session.add(sala)
        session.add(lab)
        session.commit()
        
        # Maquinas (1 em sala, 2 modelos no lab)
        m1 = Maquina(
            local_ref_id=sala.id, modelo="Dell Optiplex 7010", quantidade=1, 
            processador="i7-13700T", ram_gb=16, armazenamento_gb=512, armazenamento_tipo="SSD_NVME",
            propriedade="PROPRIO"
        )
        
        m2 = Maquina(
            local_ref_id=lab.id, modelo="Dell Optiplex 3040", quantidade=20, 
            processador="i5-6500", ram_gb=8, armazenamento_gb=256, armazenamento_tipo="SSD_SATA",
            propriedade="PROPRIO", video_vga=1, video_hdmi=1
        )
        
        m3 = Maquina(
            local_ref_id=lab.id, modelo="Lenovo V50s", quantidade=15, 
            processador="i5-10400", ram_gb=16, armazenamento_gb=512, armazenamento_tipo="SSD_NVME",
            propriedade="ALUGADO", video_dp=1, video_hdmi=1
        )
        
        session.add_all([m1, m2, m3])
        
        # Historicos
        h1 = Historico(
            local_ref_id=sala.id, local_id="S-101", status="OK", observacao="Sala mapeada e pronta", responsavel="Filipe"
        )
        h2 = Historico(
            local_ref_id=lab.id, local_id="L-01", status="PENDENTE", observacao="Faltando rede", responsavel="Filipe",
            mensagem_original="O L-01 tá quase, mas ainda falta subir a vlan e puxar pro switch novo. *L-01 Pendente*"
        )
        
        session.add_all([h1, h2])
        session.commit()
        logger.info("Seed concluído com sucesso.")
        print("Seed concluído com sucesso.")

if __name__ == "__main__":
    init_db()
