from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class KnowledgeCreate(BaseModel):
    """
    Used internally when saving parsed knowledge
    (Not for file upload directly)
    """
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    content: str


class KnowledgeResponse(BaseModel):
    """
    Response schema for Knowledge Base
    (Shown in UI knowledge list)
    """
    id: str
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
