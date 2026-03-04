import httpx
from app.config import settings
from app.logging_conf import logger

async def send_message(remote_jid: str, text: str):
    """
    Envia mensagem de texto via Evolution API.
    """
    url = f"{settings.EVOLUTION_BASE_URL}/message/sendText/{settings.EVOLUTION_INSTANCE}"
    headers = {
        "apikey": settings.EVOLUTION_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "number": remote_jid,
        "text": text,
        "delay": 1200,
        "linkPreview": False
    }
    
    logger.info(f"📤 Sending WA message to {remote_jid}: {text[:50]}...")
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code not in [200, 201]:
                logger.error(f"Failed to send WA message ({resp.status_code}): {resp.text}")
            else:
                logger.info(f"Message sent successfully to {remote_jid}")
    except Exception as e:
        logger.error(f"Exception sending WA message: {e}")
