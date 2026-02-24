from pydantic import BaseModel
from typing import Optional


class AssistantPromptCreate(BaseModel):
    """
    Prompt create/write schema
    (Used in Prompt Section UI)
    """
    first_message: Optional[str] = None
    system_prompt: Optional[str] = None
    end_call_message: Optional[str] = None


class AssistantPromptResponse(BaseModel):
    """
    Prompt response schema
    """
    assistant_id: str
    first_message: Optional[str] = None
    system_prompt: Optional[str] = None
    end_call_message: Optional[str] = None

    model_config = {
        "from_attributes": True  
    }
