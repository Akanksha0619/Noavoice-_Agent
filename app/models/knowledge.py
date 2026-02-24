import uuid
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from app.models.base import Base


class Knowledge(Base):
    __tablename__ = "knowledge"

    # Primary Key
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # File name (for UI display)
    file_name = Column(String(255), nullable=True)

    # File type (pdf, docx, txt)
    file_type = Column(String(50), nullable=True)

    # Extracted text content (MAIN KNOWLEDGE)
    content = Column(Text, nullable=False)

    # Timestamp
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
