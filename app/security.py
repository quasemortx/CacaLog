import logging

from fastapi import Header, HTTPException

from app.config import settings

logger = logging.getLogger("cacalog")


def require_webhook_token(x_cacalog_token: str | None = Header(default=None)) -> None:
    """Verifica se o token do Webhook bate com a configuração."""
    if not settings.webhook_token or settings.webhook_token == "CHANGE_ME":
        logger.warning("Token do Webhook não configurado (CHANGE_ME). Bloqueando requisição.")
        raise HTTPException(status_code=401, detail="Unauthorized")

    if x_cacalog_token != settings.webhook_token:
        logger.warning("Tentativa de acesso não autorizada ao webhook (Token inválido ou ausente).")
        raise HTTPException(status_code=401, detail="Unauthorized")


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """Verifica se a chave da API (Leitura/Painel WEB) confere."""
    if not settings.api_key:
        if settings.env == "production":
            logger.critical("API_KEY ausente em ambiente de produção!")
            raise HTTPException(status_code=500, detail="Misconfigured Server")
        return  # Permite skip de auth em local dev case não inserido

    if x_api_key != settings.api_key:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")
