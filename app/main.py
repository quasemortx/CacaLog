from fastapi import BackgroundTasks, Depends, FastAPI, Request

from app.commands import handle_command
from app.config import settings
from app.dedup import Deduper
from app.logging_conf import configure_logging, logger
from app.models import HistoryItem, InventoryItem, Status, TipoAmbiente
from app.parser import REGEX_LAB, REGEX_SALA, extract_data_regex, normalize_status
from app.redis_client import make_redis
from app.security import require_webhook_token
from app.sheets import SheetsClient
from app.utils import classify_sector, get_current_timestamp, sanitize_for_sheets
from app.whatsapp import send_message

app = FastAPI(title="CaçaLog")
redis_conn = make_redis()
deduper = Deduper(redis_conn)


# Sheets instance (global or dependency)
sheets_client = None


@app.get("/")
def read_root():
    return {"status": "CaçaLog Online", "sheets_connected": sheets_client is not None}


@app.on_event("startup")
async def startup_event():
    configure_logging()
    global sheets_client
    try:
        sheets_client = SheetsClient()
        logger.info("Connected to Google Sheets")
    except Exception as e:
        logger.critical(f"Failed to connect to Google Sheets: {e}")


@app.get("/webhook")
async def webhook_test():
    return {"status": "Webhook endpoint active (GET)"}


@app.post("/webhook")
async def webhook(
    request: Request, background_tasks: BackgroundTasks, _: None = Depends(require_webhook_token)
):
    logger.info("⚡ Webhook Request Received")
    try:
        data = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse JSON: {e}")
        return {"status": "error"}

    # Structured basic info without dumping full raw payload
    event_type = data.get("event") or data.get("type", "unknown")
    logger.info(f"📥 Event Type: {event_type}")

    if event_type not in ["messages.upsert", "message"]:
        return {"status": "ignored_event", "event": event_type}

    payload = data.get("data", {})
    key = payload.get("key", {})
    message_data = payload.get("message", {})

    remote_jid = key.get("remoteJid")
    from_me = key.get("fromMe", False)
    msg_id = key.get("id")

    # Text extraction
    conversation = message_data.get("conversation")
    if not conversation:
        conversation = message_data.get("extendedTextMessage", {}).get("text")

    if not conversation:
        return {"status": "no text"}

    # IDENTIFY SENDER (Who sent it)
    sender_jid = payload.get("sender") or key.get("participant") or remote_jid
    if from_me and not sender_jid:
        sender_jid = settings.WHATSAPP_ADMIN_ID  # Fallback for self-messages if empty

    # LOGIC UPDATE: Loop Protection / Self-Message Handling
    if from_me:
        text = conversation.strip()
        is_command = text.startswith("/") or text.startswith("!")
        # Block Bot's own outputs to prevent infinite loops
        is_bot_output = (
            text.startswith("✅") or text.startswith("⚠️") or text.startswith("Qual o status")
        )

        # Determine if it has valuable data (Room/Lab) worth parsing
        has_data = bool(REGEX_SALA.search(text) or REGEX_LAB.search(text))

        if is_bot_output:
            return {"status": "ignored_bot_reply"}

        # Allow if it's a Command OR Data Entry
        if not (is_command or has_data):
            return {"status": "ignored_self_text"}

        # If it's a command FROM ME, we process it (common when user types in WhatsApp Web)
        if is_command:
            logger.info(f"✨ Self-Command detected: {text}")

    # Only allow Group or Admin DM
    is_main_group = remote_jid == settings.WHATSAPP_GROUP_ID
    is_cmd_group = settings.WHATSAPP_CMD_GROUP_ID and remote_jid == settings.WHATSAPP_CMD_GROUP_ID
    # Admin check: Can be remoteJid (DM) or sender_jid (in Group)
    is_admin = settings.WHATSAPP_ADMIN_ID in [remote_jid, sender_jid]

    logger.info(
        f"Auth Check: source_msg={msg_id} | JID={remote_jid} | Sender={sender_jid} | Admin={is_admin} | FromMe={from_me}"
    )

    if not (is_main_group or is_cmd_group or is_admin):
        logger.warning(f"⛔ Ignored source: {remote_jid} (Sender: {sender_jid})")
        return {"status": "ignored_source", "id": remote_jid}

    # RESTRICTION: Secondary Group (Apoio a Burrices) -> COMMANDS ONLY
    if is_cmd_group:
        # Check if text is a command
        text = conversation.strip()
        is_cmd = text.startswith("/") or text.startswith("!")
        if not is_cmd:
            # We silently ignore chat in this group
            return {"status": "ignored_cmd_group_chat"}

    if await deduper.is_duplicate(msg_id):
        logger.info(f"Duplicate message ignored: {msg_id}")
        return {"status": "duplicate"}

    # Process in background
    background_tasks.add_task(process_message, conversation, msg_id, payload, remote_jid, is_admin)

    logger.info(f"✅ Webhook processed in background -> Task: {msg_id}")
    return {"status": "processing"}


async def process_message(
    text: str, msg_id: str, sender_info: dict, reply_to_jid: str, is_admin: bool = False
):
    # Sender info
    push_name = sender_info.get("pushName", "Unknown")
    sender_num = sender_info.get("participant") or sender_info.get("key", {}).get("remoteJid")

    clean_text = text.strip()
    logger.info(f"Processing Text (Msg: {msg_id} / Sender: {push_name})")

    # 1. Check for Commands
    if clean_text.startswith("/") or clean_text.startswith("!"):
        try:
            parts = clean_text.split()
            cmd = parts[0].lower()
            args = parts[1:]
            # Admin-only commands
            if cmd in ["/deletar"] and not is_admin:
                await send_message(reply_to_jid, "⛔ Apenas o admin pode usar este comando.")
                return
            response = handle_command(parts[0], args, sheets_client)
            # Record deletion in history for traceability
            if cmd == "/deletar" and response and "removido" in response:
                local_id = args[0].upper() if args else ""
                if local_id:
                    hist_item = HistoryItem(
                        timestamp=get_current_timestamp(),
                        local_id=local_id,
                        status="DELETADO",
                        observacao="Removido via comando /deletar",
                        responsavel=push_name,
                        contato=sender_num,
                        mensagem_original=clean_text,
                        message_id=msg_id,
                    )
                    sheets_client.add_history(hist_item)
            await send_message(reply_to_jid, response)
        except Exception as e:
            logger.error(f"Error processing command '{clean_text}': {e}")
            await send_message(reply_to_jid, "⚠️ Erro ao processar comando.")
        return

    # 2. Parse Inventory Data
    # Use Regex Only
    logger.info(f"Processing message with Regex (Msg: {msg_id})")
    extracted_items = extract_data_regex(clean_text)
    logger.info(f"Extracted items: {len(extracted_items)}")

    # 3. Handle Ambiguity (e.g. "390" without room)
    from app.parser import check_model_reference

    if not extracted_items:
        if check_model_reference(clean_text):
            await send_message(reply_to_jid, "⚠️ Qual sala ou laboratório isso se refere?")
            return
        logger.info("No actionable data found.")
        return

    # 4. Process Items and Persist
    results_msg = []

    for item in extracted_items:
        try:
            if not item.get("local_id"):
                continue

            current_status = normalize_status(item.get("status", "NAO_AVALIADO"))
            local_id = item["local_id"]
            logger.info(f"Processing item: {local_id} | status={current_status}")

            sanitized_obs = sanitize_for_sheets(item.get("observacao", ""))

            # Machine Types processing
            machine_types = item.get("machine_types")
            if machine_types:
                types_str = ""
                if isinstance(machine_types, dict):
                    parts = []
                    for k, v in machine_types.items():
                        parts.append(f"{k}={v}")
                    types_str = f"Tipos: {'; '.join(parts)}"
                elif isinstance(machine_types, list):
                    types_str = f"Tipos: {', '.join(machine_types)}"
                if types_str:
                    if sanitized_obs:
                        sanitized_obs += f" | {types_str}"
                    else:
                        sanitized_obs = types_str

            sector_resp = classify_sector(current_status.value, sanitized_obs)

            inv_item = InventoryItem(
                local_id=local_id,
                sala=item.get("sala", ""),
                predio=item.get("predio"),
                andar=item.get("andar"),
                tipo_ambiente=TipoAmbiente(item.get("tipo_ambiente", "SALA")),
                modelo=item.get("modelo"),
                bios=item.get("bios"),
                status=current_status,
                observacao=sanitized_obs,
                setor_responsavel=sector_resp,
                total_pcs=item.get("total_pcs", 1 if "S-" in local_id else 0),
                concluidos=item.get("concluidos", 0),
                pendentes=item.get("pendentes", 0),
                ultimo_responsavel=push_name,
                ultimo_contato=sender_num,
                ultima_atualizacao=get_current_timestamp(),
            )

            logger.info(f"Calling sheets for {local_id}...")
            existing_item = sheets_client.get_inventory_item(local_id)

            if existing_item:
                if current_status == Status.NAO_AVALIADO:
                    import contextlib
                    with contextlib.suppress(KeyError, ValueError):
                        old_s_str = existing_item.get("Status", "").upper()
                        if old_s_str in Status.__members__:
                            current_status = Status[old_s_str]
                if not item.get("modelo") and existing_item.get("Modelo"):
                    inv_item.modelo = existing_item.get("Modelo")

            if current_status == Status.NAO_AVALIADO and existing_item:
                msg_reply = f"[Info] *{local_id} está {existing_item.get('Status')}* ({existing_item.get('Modelo') or 'Modelo não def.'}).\nObs: {existing_item.get('Observacao') or '-'}"
                await send_message(reply_to_jid, msg_reply)
                return

            logger.info(f"Upserting {local_id} with status {current_status}...")
            sheets_client.upsert_inventory(inv_item)

            hist_item = HistoryItem(
                timestamp=get_current_timestamp(),
                local_id=inv_item.local_id,
                status=current_status.value,
                observacao=sanitized_obs,
                responsavel=push_name,
                contato=sender_num,
                mensagem_original=clean_text,
                message_id=msg_id,
            )
            sheets_client.add_history(hist_item)
            logger.info(f"✅ Saved {local_id} -> {current_status.value}")

            if current_status == Status.NAO_AVALIADO:
                await send_message(
                    reply_to_jid,
                    f"Qual o status de {inv_item.local_id}?\nOpções: ✅, pendente, erro, incompatível.",
                )
            else:
                results_msg.append(
                    f"✅ {inv_item.local_id} atualizado para {current_status.value}."
                )

        except Exception as e:
            logger.error(
                f"ITEM PROCESSING ERROR for '{item.get('local_id', '?')}': {e}", exc_info=True
            )
            await send_message(
                reply_to_jid, f"⚠️ Falha ao salvar {item.get('local_id', '?')}. Erro: {e}"
            )

    if results_msg:
        await send_message(reply_to_jid, "\n".join(results_msg))


@app.get("/health")
def health():
    return {"status": "ok"}
