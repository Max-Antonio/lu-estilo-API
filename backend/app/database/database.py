from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine
from sqlmodel import Session, create_engine

from app.config import settings


# Cria a engine a partir da url do banco de dados
def get_engine() -> Engine:
    return create_engine(settings.DATABASE_URL)


engine = get_engine()


def get_db():
    with Session(engine) as db:
        yield db

# Sessão do banco de dados
SessionDep = Annotated[Session, Depends(get_db)]
