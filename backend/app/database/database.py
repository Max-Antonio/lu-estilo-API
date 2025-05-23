from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine
from sqlmodel import Session, create_engine

from app.config import settings


def get_engine() -> Engine:
    return create_engine(settings.DATABASE_URL)


engine = get_engine()


def get_db():
    with Session(engine) as db:
        yield db



SessionDep = Annotated[Session, Depends(get_db)]
