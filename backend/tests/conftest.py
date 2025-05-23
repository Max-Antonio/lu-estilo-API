from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from app.database.database import get_db
from app.main import app


@pytest.fixture(name='session')
def session_fixture() -> Generator:
    """Cria una nova session como um test fixture."""
    engine = create_engine(
        'sqlite://',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name='client')
def client_fixture(session: Session) -> Generator:
    """Cria um novo cliente HTTP como um test fixture."""
    def get_db_override() -> Session:
        return session

    app.dependency_overrides[get_db] = get_db_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
