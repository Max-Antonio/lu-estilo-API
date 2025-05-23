from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from app.database.database import engine
from app.routes.auth_router import auth_router
from app.routes.usuario_router import usuario_router
from app.routes.cliente_router import cliente_router


async def init_db() -> None:
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    """Inicaliza o banco."""
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix='/auth')
app.include_router(usuario_router, prefix='/usuarios')
app.include_router(cliente_router, prefix='/clients')

