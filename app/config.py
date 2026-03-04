from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    EVOLUTION_BASE_URL: str
    EVOLUTION_INSTANCE: str
    EVOLUTION_TOKEN: str
    WHATSAPP_GROUP_ID: str
    WHATSAPP_CMD_GROUP_ID: str | None = None  # Group for Commands Only (/help, /status)
    WHATSAPP_ADMIN_ID: str | None = None  # Optional ID for private commands (Note to self)

    GOOGLE_SHEETS_ID: str
    GOOGLE_WORKSHEET_INVENTARIO: str = "Inventario"
    GOOGLE_WORKSHEET_HISTORICO: str = "Historico"
    GOOGLE_SERVICE_ACCOUNT_JSON_PATH: str

    LOG_LEVEL: str = "INFO"

    # Evolution v2 optional/new fields
    AUTHENTICATION_API_KEY: str | None = None
    DATABASE_CONNECTION_URI: str | None = None
    CACHE_REDIS_URI: str | None = None
    WEBHOOK_URL: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Allow extra fields in .env without error


settings = Settings()
