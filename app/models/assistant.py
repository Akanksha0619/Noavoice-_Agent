from sqlalchemy import Column, String, Text, Boolean, DateTime
from datetime import datetime
import uuid
from app.models.base import Base


class Assistant(Base):
    __tablename__ = "assistants"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

    # Basic Info
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Prompt Section
    first_message = Column(Text, nullable=True)
    system_prompt = Column(Text, nullable=True)
    end_call_message = Column(Text, nullable=True)

    # Voice Section
    voice_name = Column(String(100), nullable=True)
    elevenlabs_voice_id = Column(String(255), nullable=True)
    voice_provider = Column(String(100), default="elevenlabs", nullable=True)

    # Configure Section (NoaVoice Style UI)
    agent_role = Column(String(255), nullable=True)
    language = Column(String(50), default="English", nullable=True)
    timezone = Column(String(100), nullable=True)
    detect_caller_number = Column(Boolean, default=False)
    multilingual_support = Column(Boolean, default=False)
    voice_recording = Column(Boolean, default=False)

    timestamp = Column(DateTime, default=datetime.utcnow)