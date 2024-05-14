from app.config.db import Database

db_instance = Database()

def get_db():
    db_session = db_instance.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()