from sqlalchemy import create_engine, text
from config import Config

def add_status_column():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URL)
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE knowledge_notes ADD COLUMN status VARCHAR(20) DEFAULT 'pending'"))
            print("Added 'status' column.")
        except Exception as e:
            print(f"Column might already exist or error: {e}")

if __name__ == "__main__":
    add_status_column()
