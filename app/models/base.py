from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import DeclarativeBase, declarative_base
from sqlalchemy.sql import func
import uuid

class Base(DeclarativeBase):
    pass

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData

# 🔥 THIS LINE FOR CUSTOM SCHEMA
SCHEMA_NAME = "noavoice_am"

metadata = MetaData(schema=SCHEMA_NAME)

Base = declarative_base(metadata=metadata)