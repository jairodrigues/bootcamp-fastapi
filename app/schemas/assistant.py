from sqlalchemy import Column, DateTime, Integer, String
from app.config.db import Base

class AssistantSchema(Base):
    __tablename__ = "assistant"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    interaction_example = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)