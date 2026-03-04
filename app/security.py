from fastapi import Header, HTTPException

from app.config import settings


def require_webhook_token(x_cacalog_token: str | None = Header(default=None)) -> None:
    """Verifica se o token do Webhook bate com a configuração."""
    if not settings.webhook_token or settings.webhook_token == "CHANGE_ME":
        raise HTTPException(status_code=500, detail="Server misconfigured: webhook token not set")

    if x_cacalog_token != settings.webhook_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
