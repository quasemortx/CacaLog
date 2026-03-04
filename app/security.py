from fastapi import Header, HTTPException

from app.config import settings


import logging

logger = logging.getLogger("cacalog")

def require_webhook_token(x_cacalog_token: str | None = Header(default=None)) -> None:
    """Verifica se o token do Webhook bate com a configuração."""
    if not settings.webhook_token or settings.webhook_token == "CHANGE_ME":
        logger.warning("Token do Webhook não configurado (CHANGE_ME). Bloqueando requisição.")
        raise HTTPException(status_code=401, detail="Unauthorized")

    if x_cacalog_token != settings.webhook_token:
        logger.warning("Tentativa de acesso não autorizada ao webhook (Token inválido ou ausente).")
        raise HTTPException(status_code=401, detail="Unauthorized")
