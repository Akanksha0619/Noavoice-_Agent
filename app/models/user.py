from sqlalchemy import Column, String
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "client_users"  

    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    profile_image = Column(String, nullable=True)
    auth_provider = Column(String, default="google")