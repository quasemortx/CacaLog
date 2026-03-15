from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Tokens e acessos
    webhook_token: str = "CHANGE_ME"
    admin_phone: str | None = None

    # App Environment
    env: str = "development"
    log_level: str = "INFO"
    cors_origins: str = "*"

    # Web Panel Auth
    api_key: str | None = None

    # Evolution API / WhatsApp / Outros (mantendo retrocompatibilidade do que o sistema já usava)
    base_url: str | None = None
    evolution_api_key: str | None = None
    whatsapp_instance: str | None = None
    redis_url: str | None = None

    # Banco de Dados
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/cacalog"

    # Sheets e API
    GOOGLE_SERVICE_ACCOUNT_JSON_PATH: str = "./cacalog-daa224ea476d.json"
    GOOGLE_SHEETS_ID: str = ""
    GOOGLE_WORKSHEET_INVENTARIO: str = "Inventario"
    GOOGLE_WORKSHEET_HISTORICO: str = "Historico"
    
    # Auth e Evolution
    AUTHENTICATION_API_KEY: str | None = None


settings = Settings()
