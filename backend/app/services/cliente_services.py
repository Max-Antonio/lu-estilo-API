from sqlmodel import select

from app.database.database import SessionDep
from app.database.models import Cliente, Usuario
from app.database.schemas import ClienteCreate, ClienteUpdate


def get_clientes(
    db: SessionDep,
    skip: int,
    limit: int,
    nome: str | None,
    email: str | None,
) -> list[Cliente]:
    stmt = select(Cliente)
    if nome:
        stmt = stmt.join(Cliente.usuario).filter(Usuario.nome == nome)
    if email:
        stmt = stmt.join(Cliente.usuario).filter(Usuario.email == email)

    clientes = db.exec(stmt.offset(skip).limit(limit))

    return clientes


def get_cliente(db: SessionDep, cliente_id: int) -> Cliente:
    cliente = db.exec(select(Cliente).filter(Cliente.id == cliente_id)).first()
    return cliente


def create_cliente(db: SessionDep, usuario_id: int, cliente_data: ClienteCreate) -> Cliente:
    db_cliente = Cliente.model_validate(cliente_data, update={'usuario_id': usuario_id})
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


def update_cliente(db: SessionDep, cliente_data: ClienteUpdate, cliente: Cliente) -> Cliente:
    for key, value in cliente_data.model_dump(exclude_unset=True).items():
        setattr(cliente, key, value)

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    return cliente
