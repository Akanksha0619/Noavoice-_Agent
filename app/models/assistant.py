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

    # 🔥 DEFAULT TEMPLATE (AUTO SET ON CREATE)
    system_prompt = Column(
        Text,
        nullable=True,
        default="""You are a professional AI assistant for NovaVoice.
Speak in a warm, natural, and human tone.
Help users clearly and politely. Do not sound robotic."""
    )

    first_message = Column(
        Text,
        nullable=True,
        default="Hello! This is your NovaVoice AI assistant. How may I help you today?"
    )

    end_call_message = Column(
        Text,
        nullable=True,
        default="Thank you for contacting NovaVoice. Have a great day!"
    )

    # Voice Section
    voice_name = Column(String(100), nullable=True)
    elevenlabs_voice_id = Column(String(255), nullable=True)
    voice_provider = Column(String(100), default="elevenlabs", nullable=True)

    # Configure Section (Like NoaVoice UI)
    agent_role = Column(String(255), nullable=True)
    language = Column(String(50), default="English", nullable=True)
    timezone = Column(String(100), nullable=True)
    detect_caller_number = Column(Boolean, default=False)
    multilingual_support = Column(Boolean, default=False)
    voice_recording = Column(Boolean, default=False)

    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow)