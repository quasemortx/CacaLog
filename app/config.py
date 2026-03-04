from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Tokens e acessos
    webhook_token: str = "CHANGE_ME"
    admin_phone: str | None = None

    # Evolution API / WhatsApp / Outros (mantendo retrocompatibilidade do que o sistema já usava)
    base_url: str | None = None
    evolution_api_key: str | None = None
    whatsapp_instance: str | None = None

    # Sheets
    google_credentials_path: str = "credentials.json"
    google_sheet_id: str = ""


settings = Settings()
