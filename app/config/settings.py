from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ===== APP =====
    APP_NAME: str = "NoaVoiceAI"
    DEBUG: bool = True  # 🔥 ADD THIS (fixes your crash)
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    # ===== DATABASE =====
    DATABASE_URL: str

    # ===== OPENAI =====
    OPENAI_API_KEY: str

    # ===== GOOGLE OAUTH =====
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # ===== OPTIONAL SERVICES =====
    ELEVENLABS_API_KEY: str | None = None
    CAL_COM_API_KEY: str | None = None
    EVENT_TYPE_ID: str | None = None
    CAL_API_BASE_URL: str | None = None
    CAL_API_VERSION: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"  # prevent extra env crash
    )


settings = Settings()