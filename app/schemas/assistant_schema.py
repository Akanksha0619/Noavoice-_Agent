from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


# ==============================
# CREATE AGENT (ONLY BASIC FIELDS)
# ==============================
class AssistantCreate(BaseModel):
    name: str
    description: Optional[str] = None


# ==============================
# UPDATE AGENT (BASIC INFO ONLY)
# ==============================
class AssistantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# ==============================
# INTERNAL ASSISTANT DATA (FOR RESPONSE)
# ==============================
class AssistantData(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

    # Default template fields (auto set in DB)
    system_prompt: Optional[str] = None
    first_message: Optional[str] = None
    end_call_message: Optional[str] = None

    # Configure fields
    language: Optional[str] = None
    timezone: Optional[str] = None
    detect_caller_number: Optional[bool] = None
    multilingual_support: Optional[bool] = None
    voice_recording: Optional[bool] = None

    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


# ==============================
# GLOBAL RESPONSE WRAPPER (USED IN ROUTES)
# ==============================
class AssistantResponseWrapper(BaseModel):
    success: bool
    message: str
    data: Dict[str, Any]