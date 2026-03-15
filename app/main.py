from fastapi import BackgroundTasks, Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.commands import handle_command
from app.config import settings
from app.dedup import Deduper
from app.logging_conf import configure_logging, logger
from app.schemas.enums import Status, TipoAmbiente
from app.parser import REGEX_LAB, REGEX_SALA, extract_data_regex, normalize_status
from app.redis_client import make_redis
from app.security import require_webhook_token
from app.utils import classify_sector, get_current_timestamp, sanitize_for_sheets
from app.whatsapp import send_message

app = FastAPI(title="CaçaLog")
app.state.sheets_client = None

# CORS Middleware Setup
origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]

if "*" in origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

redis_conn = make_redis()
deduper = Deduper(redis_conn)


# Sheets instance (global or dependency)
sheets_client = None


@app.get("/")
def read_root():
    return {"status": "CaçaLog Online ERP"}

@app.on_event("startup")
async def startup_event():
    configure_logging()
    logger.info("Initializing system...")
    
    # Sheets Client (Descontinuado)
    global sheets_client
    try:
        from app.sheets import SheetsClient
        sheets_client = SheetsClient()
        app.state.sheets_client = sheets_client
        logger.info("Connected to Google Sheets (Legacy)")
    except Exception as e:
        logger.warning(
            f"Failed to connect to Google Sheets. Running on purely DB mode: {e}"
        )


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

    logger.info(
        f"📩 Message Info | msg_id: {msg_id} | remoteJid: {remote_jid} | event_type: {event_type} | length: {len(conversation)}"
    )

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
        return {"ok": True, "dedup": True}

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
            
            if cmd in ["/deletar"] and not is_admin:
                await send_message(reply_to_jid, "⛔ Apenas o admin pode usar este comando.")
                return
            
            # Using new DB logic for delete
            from app.db.engine import SessionLocal
            from app.models import Local, Historico
            from sqlmodel import select
            
            if cmd == "/deletar":
                local_id = args[0].upper() if args else ""
                with SessionLocal() as db:
                    loc = db.exec(select(Local).where(Local.local_id == local_id)).first()
                    if loc:
                        db.delete(loc)
                        
                        hist_item = Historico(
                            local_id=local_id,
                            status="DELETADO",
                            observacao="Removido via comando /deletar",
                            responsavel=push_name,
                            contato=sender_num,
                            mensagem_original=clean_text,
                            message_id=msg_id,
                        )
                        db.add(hist_item)
                        db.commit()
                        await send_message(reply_to_jid, f"✅ {local_id} deletado com sucesso do banco de dados (Novo).")
                    else:
                        await send_message(reply_to_jid, f"⚠️ Local {local_id} não encontrado no banco.")
                return
                
            # Legacy commands fallback
            if sheets_client:
                response = handle_command(parts[0], args, sheets_client)
                await send_message(reply_to_jid, response)
            else:
                await send_message(reply_to_jid, "⚠️ Comandos legados desativados nesta versão da API.")
                
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

            sector_resp = classify_sector(current_status.value, sanitized_obs)

            # DB Write
            from app.db.engine import SessionLocal
            from app.models import Local, Historico
            from sqlmodel import select
            from datetime import datetime
            
            with SessionLocal() as db:
                loc = db.exec(select(Local).where(Local.local_id == local_id)).first()
                if not loc:
                    total = item.get("total_pcs", 1 if "S-" in local_id else 0)
                    loc = Local(
                        local_id=local_id,
                        sala=item.get("sala", ""),
                        tipo_local="SALA" if "S-" in local_id else "LAB",
                        predio=item.get("predio"),
                        andar=item.get("andar"),
                        tipo_ambiente=item.get("tipo_ambiente", "SALA"),
                        status=current_status.value,
                        observacao=sanitized_obs,
                        setor=sector_resp,
                        ultimo_responsavel=push_name,
                        ultimo_contato=sender_num,
                        updated_at=datetime.utcnow()
                    )
                    db.add(loc)
                else:
                    if current_status == Status.NAO_AVALIADO:
                        # restore status safely
                        current_status = Status(loc.status) if loc.status else Status.NAO_AVALIADO
                        
                    loc.status = current_status.value
                    if sanitized_obs:
                        loc.observacao = sanitized_obs
                    loc.ultimo_responsavel = push_name
                    loc.ultimo_contato = sender_num
                    loc.updated_at = datetime.utcnow()
                    db.add(loc)
                    
                db.commit()
                db.refresh(loc)
                
                hist_item = Historico(
                    local_ref_id=loc.id,
                    local_id=loc.local_id,
                    status=current_status.value,
                    observacao=sanitized_obs,
                    responsavel=push_name,
                    contato=sender_num,
                    mensagem_original=clean_text,
                    message_id=msg_id,
                )
                db.add(hist_item)
                db.commit()

            logger.info(f"✅ Saved {local_id} -> {current_status.value} (DB)")

            if current_status == Status.NAO_AVALIADO:
                await send_message(
                    reply_to_jid,
                    f"Qual o status de {local_id}?\nOpções: ✅, pendente, erro, incompatível.",
                )
            else:
                results_msg.append(
                    f"✅ {local_id} atualizado para {current_status.value}."
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
    return {"status": "ok", "db_connected": True}


# Registrar router da API no final para evitar circulares ou usar injeção seprada
def register_routes() -> None:
    from app.api import router as api_router  # import local para evitar circular

    app.include_router(api_router)


register_routes()
