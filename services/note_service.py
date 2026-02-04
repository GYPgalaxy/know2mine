from sqlalchemy.orm import Session
from models import KnowledgeNote
import datetime
from typing import List

class NoteService:
    def __init__(self, db: Session):
        self.db = db

    def create_note(self, content: str):
        note = KnowledgeNote(content=content)
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def get_note_by_id(self, note_id: int):
        return self.db.query(KnowledgeNote).filter(KnowledgeNote.id == note_id).first()

    def update_note_status(self, note_id: int, status: str):
        note = self.db.query(KnowledgeNote).filter(KnowledgeNote.id == note_id).first()
        if note:
            note.status = status
            self.db.commit()
            self.db.refresh(note)
        return note

    def update_note_ai_data(self, note_id: int, category: str, tags: list, embedding: list):
        note = self.db.query(KnowledgeNote).filter(KnowledgeNote.id == note_id).first()
        if note:
            note.category = category
            note.tags = tags
            note.embedding = embedding
            self.db.commit()
            self.db.refresh(note)
        return note

    def get_active_notes(self):
        return self.db.query(KnowledgeNote).filter(KnowledgeNote.is_deleted == False).order_by(KnowledgeNote.created_at.desc()).all()

    def get_deleted_notes(self):
        return self.db.query(KnowledgeNote).filter(KnowledgeNote.is_deleted == True).order_by(KnowledgeNote.deleted_at.desc()).all()

    def soft_delete_notes(self, note_ids: List[int]):
        self.db.query(KnowledgeNote).filter(KnowledgeNote.id.in_(note_ids)).update({
            KnowledgeNote.is_deleted: True,
            KnowledgeNote.deleted_at: datetime.datetime.now()
        }, synchronize_session=False)
        self.db.commit()

    def restore_notes(self, note_ids: List[int]):
        self.db.query(KnowledgeNote).filter(KnowledgeNote.id.in_(note_ids)).update({
            KnowledgeNote.is_deleted: False,
            KnowledgeNote.deleted_at: None
        }, synchronize_session=False)
        self.db.commit()

    def hard_delete_notes(self, note_ids: List[int]):
        self.db.query(KnowledgeNote).filter(KnowledgeNote.id.in_(note_ids)).delete(synchronize_session=False)
        self.db.commit()

    def empty_recycle_bin(self):
        self.db.query(KnowledgeNote).filter(KnowledgeNote.is_deleted == True).delete(synchronize_session=False)
        self.db.commit()
        
    def cleanup_old_deleted_notes(self, days=30):
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
        self.db.query(KnowledgeNote).filter(
            KnowledgeNote.is_deleted == True,
            KnowledgeNote.deleted_at < cutoff_date
        ).delete(synchronize_session=False)
        self.db.commit()
