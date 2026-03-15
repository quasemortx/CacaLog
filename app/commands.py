import contextlib
from app.db.engine import SessionLocal
from app.models import Local, Maquina, Historico
from app.schemas.enums import Status
from sqlmodel import select, func
import logging

logger = logging.getLogger("commands")

def handle_command(command: str, args: list[str]) -> str:
    # Normalize: remove whitespace, lower, handle ! or /
    cmd = command.strip().lower()
    if cmd.startswith("!"):
        cmd = "/" + cmd[1:]

    logger.info(f"Command received: '{cmd}' Args: {args}")

    if cmd == "/help":
        return """📟 CAÇALOG — GUIA DE COMANDOS

━━━━━━━━━━━━━━━━━━━━
📄 AJUDA
━━━━━━━━━━━━━━━━━━━━

/help
→ Mostra todos os comandos disponíveis.

/status <sala>
→ Mostra status atual da sala.
Ex: /status 712

/lab <id>
→ Mostra status do laboratório.
Ex: /lab 03

━━━━━━━━━━━━━━━━━━━━
🚨 LISTAGENS GERAIS
━━━━━━━━━━━━━━━━━━━━

/pendentes
→ Lista TODAS as salas e labs com status PENDENTE.

/erros
→ Lista todos os locais com ERRO.

/incompativeis
→ Lista locais INCOMPATÍVEIS.

━━━━━━━━━━━━━━━━━━━━
📊 RESUMOS POR PRÉDIO
━━━━━━━━━━━━━━━━━━━━

/resumo p1
→ Resumo geral do prédio 1.

/resumo p2
→ Resumo geral do prédio 2.

━━━━━━━━━━━━━━━━━━━━
🧪 LABORATÓRIOS
━━━━━━━━━━━━━━━━━━━━

/labs
→ Lista TODOS os laboratórios.

━━━━━━━━━━━━━━━━━━━━
🗑️ REMOÇÃO
━━━━━━━━━━━━━━━━━━━━

/deletar <id>
→ Remove uma sala ou lab do inventário.
⚠️ Apenas admin pode usar.
Ex: /deletar S-712 ou /deletar L-03
"""

    with SessionLocal() as session:
        if cmd == "/status":
            if not args:
                return "Uso: /status [sala]"
            
            target = " ".join(args).lower()
            
            # Simple search in DB
            statement = select(Local).where(
                (func.lower(Local.local_id).contains(target)) | 
                (func.lower(Local.sala).contains(target))
            )
            found = session.exec(statement).all()
            
            if not found:
                return f"Não encontrado: {target}"
            
            resp = ""
            for loc in found:
                resp += f"✅ {loc.local_id}: {loc.status or 'NAO AVALIADO'} ({loc.observacao or 'Sem obs'})\n"
            return resp.strip()

        if cmd == "/lab":
            if not args:
                return "Uso: /lab [numero]"
            raw_arg = args[0]
            
            # Try variations: "03" -> "L-03"
            target_ids = [f"L-{raw_arg}"]
            if raw_arg.isdigit():
                target_ids.append(f"L-{int(raw_arg):02d}")
                target_ids.append(f"L-{int(raw_arg)}")
            
            statement = select(Local).where(Local.local_id.in_(target_ids))
            found = session.exec(statement).all()
            
            if not found:
                return "Lab não encontrado."
            
            resp = ""
            for loc in found:
                resp += f"{loc.local_id} ({loc.tipo_local}): {loc.status}\nObs: {loc.observacao or 'Sem obs'}\n"
            return resp.strip()

        if cmd in ["/pendentes", "/erros", "/incompativeis"]:
            target_status = {
                "/pendentes": "PENDENTE",
                "/erros": "ERRO",
                "/incompativeis": "INCOMPATIVEL"
            }[cmd]
            
            statement = select(Local).where(Local.status == target_status)
            found = session.exec(statement).all()
            
            if not found:
                return f"Nenhum registro com status {target_status}."
            
            resp = f"Lista de {target_status}:\n"
            for loc in found[:40]:
                resp += f"🔸 {loc.local_id}: {loc.status} ({loc.observacao or 'Sem obs'})\n"
            if len(found) > 40:
                resp += "...e mais."
            return resp

        if cmd == "/resumo":
            if not args:
                return "Uso: /resumo p1 ou p2"
            predio_arg = args[0].lower()
            if predio_arg not in ["p1", "p2"]:
                return "Prédio inválido."
            
            p_num = 1 if predio_arg == "p1" else 2
            
            # Rooms Summary
            salas_stmt = select(Local).where(Local.predio == p_num, Local.tipo_local == "SALA")
            salas = session.exec(salas_stmt).all()
            
            # Labs Summary
            labs_stmt = select(Local).where(Local.predio == p_num, Local.tipo_local == "LAB")
            labs = session.exec(labs_stmt).all()
            
            def get_stats(loc_list):
                total = len(loc_list)
                ok = len([l for l in loc_list if l.status == "OK"])
                pend = len([l for l in loc_list if l.status == "PENDENTE"])
                erro = len([l for l in loc_list if l.status == "ERRO"])
                return total, ok, pend, erro

            resp = f"📊 **Resumo Prédio {p_num}**\n\n"
            
            st_t, st_ok, st_p, st_e = get_stats(salas)
            resp += f"🏢 **Salas** (Total: {st_t}):\n✅ OK: {st_ok}\n⏳ Pend: {st_p}\n⚠️ Erro: {st_e}\n\n"
            
            lb_t, lb_ok, lb_p, lb_e = get_stats(labs)
            resp += f"🧪 **Laboratórios** (Total: {lb_t}):\n✅ OK: {lb_ok}\n⏳ Pend: {lb_p}\n⚠️ Erro: {lb_e}\n"
            
            return resp.strip()

        if cmd == "/labs":
            statement = select(Local).where(Local.tipo_local == "LAB")
            found = session.exec(statement).all()
            
            if not found:
                return "Nenhum lab registrado."
            
            resp = "🧪 **Status Laboratórios:**\n"
            for loc in found:
                resp += f"🔸 {loc.local_id}: {loc.status or 'NAO AVALIADO'}\n"
            return resp

    return "Comando desconhecido ou Legacy desativado."
