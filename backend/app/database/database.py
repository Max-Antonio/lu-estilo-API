from sqlmodel import create_engine
from sqlalchemy import Engine
from app.config import settings
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.database.models import Usuario

def get_engine() -> Engine:
    return create_engine(settings.DATABASE_URL)


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()