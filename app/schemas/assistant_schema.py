from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AssistantBase(BaseModel):
    name: str
    description: Optional[str] = None


class AssistantCreate(AssistantBase):
    pass


class AssistantResponse(AssistantBase):
    id: str
    timestamp: Optional[datetime] = None  

    class Config:
        from_attributes = True
