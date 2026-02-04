import os
import redis
from rq import Worker, Queue, Connection
from config import Config
from database import get_db
from services.note_service import NoteService
from services.ai_service import AIService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

listen = ['default']

def process_note_ai(note_id: int):
    """
    Background task to process AI for a note.
    """
    logger.info(f"Processing note {note_id}...")
    
    # Create new DB session for this task
    db = next(get_db())
    note_service = NoteService(db)
    ai_service = AIService()
    
    try:
        # Get note content
        note = note_service.get_note_by_id(note_id)
        if not note:
            logger.error(f"Note {note_id} not found.")
            return

        # Update status to processing
        note_service.update_note_status(note_id, "processing")

        # Process
        content = note.content
        
        # Note: Worker needs to pick up the correct provider. 
        # Since Config is loaded at start, dynamic changes in UI might not propagate to worker 
        # unless passed as arguments or stored in DB/Redis.
        # For this phase, we assume the worker uses the default .env Config or we'd need to enhance architecture.
        # To make it robust, we'll instantiate AIService inside the task, which reads Config.
        # But Config.AI_PROVIDER is static from env. 
        # IMPROVEMENT: Pass provider in the job arguments if per-request provider is needed.
        
        ai_data = ai_service.classify_and_tag(content)
        embedding = ai_service.generate_embedding(content)
        
        # Save results
        note_service.update_note_ai_data(
            note_id=note.id,
            category=ai_data.get("category"),
            tags=ai_data.get("tags"),
            embedding=embedding
        )
        
        # Update status to completed
        note_service.update_note_status(note_id, "completed")
        logger.info(f"Note {note_id} processed successfully.")
        
    except Exception as e:
        logger.error(f"Error processing note {note_id}: {e}")
        note_service.update_note_status(note_id, "failed")
    finally:
        db.close()

if __name__ == '__main__':
    conn = redis.from_url(f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/{Config.REDIS_DB}")
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
