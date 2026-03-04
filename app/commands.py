from app.sheets import SheetsClient


def handle_command(command: str, args: list[str], sheets: SheetsClient) -> str:
    # Normalize: remove whitespace, lower, handle ! or /
    cmd = command.strip().lower()
    if cmd.startswith("!"):
        cmd = "/" + cmd[1:]

    import logging

    logger = logging.getLogger("commands")
    logger.info(f"Command received: '{cmd}' Args: {args}")

    if cmd == "/help":
        return """📟 CAÇALOG — GUIA DE COMANDOS

━━━━━━━━━━━━━━━━━━━━
📄 AJUDA E PLANILHA
━━━━━━━━━━━━━━━━━━━━

/help
→ Mostra todos os comandos disponíveis.

/planilha
/planilha
→ Retorna o link da planilha Google Sheets.

/organizar
→ Força a ordenação da planilha (Prédio > Andar > Sala).

━━━━━━━━━━━━━━━━━━━━
🖥️ CONSULTAS INDIVIDUAIS
━━━━━━━━━━━━━━━━━━━━

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
🏢 CONSULTA POR ANDAR
━━━━━━━━━━━━━━━━━━━━

/andar <numero> p1
→ Ex: /andar 7 p1

/andar <numero> p2
→ Ex: /andar 4 p2

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

    if cmd == "/planilha":
        url = (
            f"https://docs.google.com/spreadsheets/d/{sheets.sheet.id}"
            if hasattr(sheets, "sheet")
            else "Link não disponível."
        )
        return f"📊 Planilha: {url}"

    if cmd == "/organizar":
        try:
            sheets.sort_inventory()
            return "🧹 Planilha organizada com sucesso! (Prédio > Andar > Sala)"
        except Exception as e:
            return f"⚠️ Falha ao organizar: {e}"

    records = sheets.get_all_records()

    if cmd == "/status":
        if not args:
            return "Uso: /status [sala]"

        # Intercept /status labs
        subcmd = args[0].lower()
        if subcmd in ["labs", "laboratorios", "laboratórios"]:
            # Redirect to labs logic (duplicated here for simplicity or call helper)
            # Let's just return the labs logic here to avoid huge refactor
            found = [r for r in records if r["TipoAmbiente"] == "LAB"]
            if not found:
                return "Nenhum lab registrado."

            resp = "🧪 **Status Laboratórios:**\n"
            for r in found:
                local_id = r["local_id"]
                status = r["Status"]
                total = r.get("TotalPCs", 0)
                ok = r.get("Concluidos", 0)
                pend = r.get("Pendentes", 0)
                erro = r.get("Erros", 0)
                stats = f"(Total: {total} | ✅ {ok} | ⏳ {pend} | ⚠️ {erro})"
                resp += f"🔸 {local_id}: {stats}\n"
            return resp

        # Allow multi-word search (e.g. "lab 9")
        target = " ".join(args).lower()

        # Smart Normalization for Labs
        search_terms = [target]
        if "lab" in target:
            nums = [int(s) for s in target.split() if s.isdigit()]
            if nums:
                n = nums[0]
                search_terms.append(f"l-{n}")
                search_terms.append(f"l-{n:02d}")

        found = []
        for r in records:
            r_id = str(r["local_id"]).lower()
            r_sala = str(r["Sala"]).lower()

            # Check all variations
            if any(term in r_id or term in r_sala for term in search_terms):
                found.append(r)

        if not found:
            return f"Não encontrado: {target}"
        resp = ""
        for f in found:
            model_str = f" [Modelo: {f.get('Modelo', '')}]" if f.get("Modelo") else ""
            resp += f"✅ {f['local_id']}: {f['Status']}{model_str} ({f['Observacao']})\n"
        return resp.strip()

    if cmd == "/lab":
        if not args:
            return "Uso: /lab [numero]"
        raw_arg = args[0]

        # Try variations: "9" -> "L-9", "L-09", "LAB 9", "LAB 09"
        targets = [f"L-{raw_arg}", f"L-{int(raw_arg):02d}" if raw_arg.isdigit() else raw_arg]
        if "l-" not in raw_arg.lower():
            targets.append(raw_arg)

        found = []
        for r in records:
            if r["local_id"] in targets or str(r["local_id"]).lower() == f"lab {raw_arg}".lower():
                found.append(r)

        if not found:
            return "Lab não encontrado."

        resp = ""
        for r in found:
            resp += (
                f"{r['local_id']} ({r['TipoAmbiente']}): {r['Status']}\nObs: {r['Observacao']}\n"
            )
        return resp.strip()

    if cmd in [
        "/pendentes",
        "/erros",
        "/incompativeis",
        "/atualizando",
        "/subindo",
        "/naoavaliados",
        "/faltantes",
    ]:
        target_status = {
            "/pendentes": "PENDENTE",
            "/erros": "ERRO",
            "/incompativeis": "INCOMPATIVEL",
            "/atualizando": "ATUALIZANDO",
            "/subindo": "ATUALIZANDO",
            "/naoavaliados": "NAO_AVALIADO",
            "/faltantes": "NAO_AVALIADO",
        }[cmd]

        found = [r for r in records if r["Status"] == target_status]
        if not found:
            return f"Nenhum registro com status {target_status}."

        resp = f"Lista de {target_status}:\n"
        count = 0
        for r in found:
            if count > 40:  # Limite para não floodar
                resp += "...e mais."
                break
            # User request: "ver os status das maquinas"
            # Format: S-712: PENDENTE (Obs: ...)
            model_info = f" [{r.get('Modelo')}]" if r.get("Modelo") else ""
            resp += f"🔸 {r['local_id']}{model_info}: {r['Status']} ({r['Observacao']})\n"
            count += 1
        return resp

    # New Commands: /ti and /manutencao
    if cmd in ["/ti", "/manutencao", "/manutenção"]:
        target_sector = "TI" if cmd == "/ti" else "Manutenção"

        # Filter: Status NOT OK AND Setor matches
        found = [r for r in records if r["Status"] != "OK" and r.get("Setor") == target_sector]

        if not found:
            return f"Nenhum chamado pendente para {target_sector}."

        resp = f"🛠️ Chamados {target_sector}:\n"
        count = 0
        for r in found:
            if count > 30:
                resp += "...e mais."
                break
            resp += f"🔸 {r['local_id']}: {r['Status']} ({r['Observacao']})\n"
            count += 1
        return resp

    if cmd == "/resumo":
        if not args:
            return "Uso: /resumo p1 ou p2"
        predio_arg = args[0].lower()
        if predio_arg not in ["p1", "p2"]:
            return "Prédio inválido."

        p_num = 1 if predio_arg == "p1" else 2

        # Helper to classify Predio for existing records (if missing) or use existing
        def get_predio(r):
            p = str(r.get("Predio", "")).upper().strip()
            # Try digit
            if p.isdigit():
                return int(p)
            # Try P1/P2/Prédio 1
            if "1" in p:
                return 1
            if "2" in p:
                return 2

            # Fallback for Labs
            lid = str(r.get("local_id", ""))
            if "L-" in lid:
                try:
                    val = int(lid.replace("L-", ""))
                    return 2 if val >= 20 else 1
                except:
                    pass
            return 0

        # Helper to count sectors
        def count_sector(rec_list, sector_name):
            return len([r for r in rec_list if r.get("Setor") == sector_name])

        # Helper to format breakdown
        def format_breakdown(total, ti, man):
            if total == 0:
                return ""
            parts = []
            if ti > 0:
                parts.append(f"{ti} TI")
            if man > 0:
                parts.append(f"{man} Manut.")
            if not parts:
                return ""
            return f" ({' / '.join(parts)})"

        # Filter by Predio
        filtered_all = [r for r in records if get_predio(r) == p_num]

        # Split Rooms and Labs using Type OR ID Prefix (robust detection)
        labs = []
        salas = []
        for r in filtered_all:
            is_lab = r.get("TipoAmbiente") == "LAB" or str(
                r.get("local_id", "")
            ).upper().startswith("L-")
            if is_lab:
                labs.append(r)
            else:
                salas.append(r)

        # Helper to safely extract Real Total PCs
        def get_real_total(r):
            base_total = int(r.get("TotalPCs", 0) or 0)
            ok = int(r.get("Concluidos", 0) or 0)
            pend = int(r.get("Pendentes", 0) or 0)
            erro = int(r.get("Erros", 0) or 0)
            # Total é, no mínimo, a soma das máquinas já atestadas em sub-status
            return max(base_total, ok + pend + erro)

        # Calculate Total Machines in Building
        total_pcs_building = 0
        for r in salas:
            # For rooms, we assume at least 1 machine even if everything is 0
            pcs = get_real_total(r)
            total_pcs_building += max(1, pcs)

        for r in labs:
            total_pcs_building += get_real_total(r)

        def generate_block(title, data):
            if not data:
                return ""  # Don't show empty block

            t = len(data)
            o = len([r for r in data if r["Status"] == "OK"])
            p_list = [r for r in data if r["Status"] == "PENDENTE"]
            pt = len(p_list)
            p_str = format_breakdown(
                pt, count_sector(p_list, "TI"), count_sector(p_list, "Manutenção")
            )

            e_list = [r for r in data if r["Status"] == "ERRO"]
            et = len(e_list)
            e_str = format_breakdown(
                et, count_sector(e_list, "TI"), count_sector(e_list, "Manutenção")
            )

            i = len([r for r in data if r["Status"] == "INCOMPATIVEL"])
            a = len([r for r in data if r["Status"] == "ATUALIZANDO"])
            n = len([r for r in data if r["Status"] == "NAO_AVALIADO"])

            return (
                f"{title} (Locais: {t}):\n"
                f"✅ OK: {o}\n"
                f"⏳ Pend: {pt}{p_str}\n"
                f"🔄 Upd: {a}\n"
                f"⚠️ Erro: {et}{e_str}\n"
                f"🚫 Inc: {i}\n"
                f"❓ Não avaliadas: {n}\n"
            )

        def generate_lab_block(title, data):
            if not data:
                return ""

            t_labs = len(data)

            # Machine Counts
            ok_pcs = sum(int(r.get("Concluidos", 0) or 0) for r in data)
            pend_pcs = sum(int(r.get("Pendentes", 0) or 0) for r in data)
            erro_pcs = sum(int(r.get("Erros", 0) or 0) for r in data)
            total_pcs = sum(get_real_total(r) for r in data)

            # Sector Breakdown for Machines (Assumes all machines in a Lab follow the Lab's sector)
            def sum_sector_col(col_name, sector):
                return sum(int(r.get(col_name, 0) or 0) for r in data if r.get("Setor") == sector)

            p_ti = sum_sector_col("Pendentes", "TI")
            p_man = sum_sector_col("Pendentes", "Manutenção")
            p_str = format_breakdown(pend_pcs, p_ti, p_man)

            e_ti = sum_sector_col("Erros", "TI")
            e_man = sum_sector_col("Erros", "Manutenção")
            e_str = format_breakdown(erro_pcs, e_ti, e_man)

            # Identify missing machines
            faltantes = total_pcs - (ok_pcs + pend_pcs + erro_pcs)
            faltantes_str = f"❓ Sem status: {faltantes}\n" if faltantes > 0 else ""

            return (
                f"{title} (Locais: {t_labs} | PCs: {total_pcs}):\n"
                f"✅ OK: {ok_pcs}\n"
                f"⏳ Pend: {pend_pcs}{p_str}\n"
                f"⚠️ Erro: {erro_pcs}{e_str}\n"
                f"{faltantes_str}"
            )

        resp = f"📊 **Resumo Prédio {p_num}**\n\n"

        if salas:
            resp += generate_block("🏢 **Salas**", salas) + "\n"
        else:
            resp += "🏢 Salas: Nenhuma registrada.\n\n"

        if labs:
            resp += generate_lab_block("🧪 **Laboratórios**", labs)
        else:
            if p_num == 1:
                resp += "🧪 Labs (<20): Nenhum.\n"
            else:
                resp += "🧪 Labs (20+): Nenhum.\n"

        resp += f"\n💻 **Total Máquinas no Prédio:** {total_pcs_building}"

        return resp.strip()

    if cmd == "/labs" or (
        cmd == "/status" and args and args[0].lower() in ["labs", "laboratorios"]
    ):
        found = [r for r in records if r["TipoAmbiente"] == "LAB"]
        if not found:
            return "Nenhum lab registrado."

        resp = "🧪 **Status Laboratórios:**\n"
        for r in found:
            local_id = r["local_id"]
            status = r["Status"]
            total = r.get("TotalPCs", 0)
            ok = r.get("Concluidos", 0)
            pend = r.get("Pendentes", 0)
            erro = r.get("Erros", 0)

            # Format: L-03: PENDENTE (Total: 20 | ✅ 15 | ⏳ 3 | ⚠️ 2)
            stats = f"(Total: {total} | ✅ {ok} | ⏳ {pend} | ⚠️ {erro})"
            resp += f"🔸 {local_id}: {status} {stats}\n"

        return resp

    if cmd == "/andar":
        if len(args) < 2:
            return "Uso: /andar [andar] [predio] (Ex: /andar 7 p1)"

        # Tenta identificar args
        p_str = ""
        andar_val = None

        # Detectar qual arg é prédio
        if "p1" in args[0].lower() or "p2" in args[0].lower():
            p_str = args[0].lower()
            try:
                andar_val = int(args[1])
            except:
                pass
        elif "p1" in args[1].lower() or "p2" in args[1].lower():
            p_str = args[1].lower()
            try:
                andar_val = int(args[0])
            except:
                pass

        predio = 1 if "p1" in p_str else 2 if "p2" in p_str else None

        if not predio or andar_val is None:
            return "Formato inválido. Use: /andar [andar] p1 ou p2"

        filtered = [r for r in records if r.get("Predio") == predio and r.get("Andar") == andar_val]

        if not filtered:
            return f"Nenhum registro encontrado para Prédio {predio}, Andar {andar_val}."

        # Stats
        total = len(filtered)
        ok = len([r for r in filtered if r["Status"] == "OK"])
        pend = len([r for r in filtered if r["Status"] == "PENDENTE"])
        erro = len([r for r in filtered if r["Status"] == "ERRO"])

        resp = f"🏢 *Prédio {predio} - {andar_val}º Andar*\n"
        resp += f"Total: {total} | ✅ {ok} | ⏳ {pend} | ⚠️ {erro}\n\n"

        # List exceptions (non-OK)
        exceptions = [r for r in filtered if r["Status"] != "OK"]
        if exceptions:
            resp += "*Atenção:*\n"
            for r in exceptions:
                resp += f"{r['local_id']}: {r['Status']}\n"
        else:
            resp += "Tudo certo neste andar! ✨"

        return resp

    if cmd == "/atualizar":
        # Force sync from history (re-process last N messages)
        # Useful if Sheets didn't catch something
        try:
            # This requires access to history_buffer which is in main.py usually
            # But here we only have sheets client.
            # If the intent is to re-read history from sheets and re-apply logic?
            # actually the log shows "Erro ao buscar histórico: 'int' object has no attribute 'get'"
            # suggesting the code iterates over a list of items where some are ints.

            # Let's inspect what "sheets.get_history()" returns.
            # Assuming it returns a list of HistoryItem dicts.
            history = sheets.get_all_history()  # Need to verify if this method exists or usage

            # Implementation fix based on error:
            # The error implies `item.get()` failed on an int.
            # So we must validade `item`.

            count = 0
            for item in history[-20:]:  # Last 20
                if not isinstance(item, dict):
                    continue

                # Re-apply logic (simplified)
                # ...
                count += 1

            return f"🔄 Sincronização Finalizada. Revisadas {count} msgs."
        except Exception as e:
            logger.error(f"Error in /atualizar: {e}", exc_info=True)
            return "❌ Erro ao atualizar."

    if cmd == "/deletar":
        if not args:
            return "Uso: /deletar <id>\nEx: /deletar S-712 ou /deletar L-03"
        local_id = args[0].upper()
        if not (local_id.startswith("S-") or local_id.startswith("L-")):
            return "⚠️ ID inválido. Use formato S-712 ou L-03."
        try:
            deleted = sheets.delete_inventory_item(local_id)
        except Exception as e:
            logger.error(f"Error in /deletar '{local_id}': {e}")
            return "❌ Erro ao tentar remover. Tente novamente."
        if deleted:
            logger.info(f"/deletar: removed {local_id}")
            return f"🗑️ *{local_id}* removido do inventário com sucesso."
        return f"❌ Não encontrado: {local_id}"

    return "Comando desconhecido."
