from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from database import Base
import datetime

class KnowledgeNote(Base):
    __tablename__ = "knowledge_notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    category = Column(String(50), nullable=True)
    tags = Column(JSON, nullable=True)  # List of strings
    embedding = Column(JSON, nullable=True) # List of floats
    status = Column(String(20), default="pending") # pending, completed, failed
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    is_deleted = Column(Boolean, default=False, index=True)
    deleted_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "category": self.category,
            "tags": self.tags,
            "created_at": self.created_at,
            "is_deleted": self.is_deleted,
            "deleted_at": self.deleted_at
        }
