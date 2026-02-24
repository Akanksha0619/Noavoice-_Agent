import uuid
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector  # NEW
from app.models.base import Base


class Knowledge(Base):
    __tablename__ = "knowledge"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    file_name = Column(String(255), nullable=True)
    file_type = Column(String(50), nullable=True)

  
    content = Column(Text, nullable=False)

   
    embedding = Column(Vector(384), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )