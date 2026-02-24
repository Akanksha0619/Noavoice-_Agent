from sqlalchemy import Column, String, Text, Boolean, DateTime
from datetime import datetime
import uuid
from app.models.base import Base


class Assistant(Base):
    __tablename__ = "assistants"

    # Primary
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

    # Basic Info
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Prompt Section (Prompt UI)
    first_message = Column(Text, nullable=True)
    system_prompt = Column(Text, nullable=True)
    end_call_message = Column(Text, nullable=True)

    # Voice Section (Voice UI)
    voice_name = Column(String(100), nullable=True)
    elevenlabs_voice_id = Column(String(255), nullable=True)

    # Configure Section (THIS WAS MISSING → caused your error)
    language = Column(String(50), default="English", nullable=True)
    timezone = Column(String(100), nullable=True)
    detect_caller_number = Column(Boolean, default=False)
    multilingual_support = Column(Boolean, default=False)

    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow)
