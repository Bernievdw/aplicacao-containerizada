from sqlmodel import create_engine, SQLModel, Session
from app.backend.core.config import get_settings

settings = get_settings()

# Use echo=True for debug logs
engine = create_engine(settings.DATABASE_URL, echo=False, future=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
