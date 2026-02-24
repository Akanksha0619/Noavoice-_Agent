from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
class Settings(BaseSettings):
    # App
    APP_NAME: str = "NoaVoiceAI"
    DEBUG: bool = False
    
    # Cal.com V2
    CALCOM_API_KEY: str
    CALCOM_EVENT_TYPE_ID: int
    CALCOM_BASE_URL: str = "https://api.cal.com/v2"
    CALCOM_API_VERSION: str = "2024-08-13"
    
    # Neon PostgreSQL
    DATABASE_URL: str

    # 🔊 ElevenLabs
    ELEVENLABS_API_KEY: str
    ELEVENLABS_MODEL_ID: str = "eleven_multilingual_v2"


    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"



    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.
    Import and call get_settings() anywhere in the app.
    """
    return Settings()
