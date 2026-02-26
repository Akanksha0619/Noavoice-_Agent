from pydantic import BaseModel
from typing import Optional


class AssistantConfigureUpdate(BaseModel):
    # Basic Config (UI fields)
    agent_role: Optional[str] = None
    language: Optional[str] = "English"
    timezone: Optional[str] = None

    # Voice Config (IMPORTANT)
    voice_name: Optional[str] = None
    elevenlabs_voice_id: Optional[str] = None
    voice_provider: Optional[str] = "elevenlabs"

    # Toggles
    detect_caller_number: Optional[bool] = False
    multilingual_support: Optional[bool] = False
    voice_recording: Optional[bool] = False


class AssistantConfigureResponse(BaseModel):
    assistant_id: str
    agent_role: Optional[str] = None

    voice_name: Optional[str] = None
    elevenlabs_voice_id: Optional[str] = None
    voice_provider: Optional[str] = None

    language: Optional[str] = None
    timezone: Optional[str] = None
    detect_caller_number: Optional[bool] = None
    multilingual_support: Optional[bool] = None
    voice_recording: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }