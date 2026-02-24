from pydantic import BaseModel
from typing import Optional


class AssistantConfigureCreate(BaseModel):
    """
    Configure Section (Voice + Settings)
    Used in Configure Assistant UI (NoaVoice style)
    """
    voice_name: Optional[str] = None
    elevenlabs_voice_id: Optional[str] = None
    language: Optional[str] = "English"
    timezone: Optional[str] = None
    detect_caller_number: Optional[bool] = False
    multilingual_support: Optional[bool] = False


class AssistantConfigureResponse(BaseModel):
    """
    Configure response schema
    """
    assistant_id: str
    voice_name: Optional[str] = None
    elevenlabs_voice_id: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    detect_caller_number: Optional[bool] = None
    multilingual_support: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }
from pydantic import BaseModel
from typing import Optional


class AssistantConfigureCreate(BaseModel):
    """
    Configure Section (Voice + Settings)
    Used in Configure Assistant UI (NoaVoice style)
    """
    voice_name: Optional[str] = None
    elevenlabs_voice_id: Optional[str] = None
    language: Optional[str] = "English"
    timezone: Optional[str] = None
    detect_caller_number: Optional[bool] = False
    multilingual_support: Optional[bool] = False


class AssistantConfigureResponse(BaseModel):
    """
    Configure response schema
    """
    assistant_id: str
    voice_name: Optional[str] = None
    elevenlabs_voice_id: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    detect_caller_number: Optional[bool] = None
    multilingual_support: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }
