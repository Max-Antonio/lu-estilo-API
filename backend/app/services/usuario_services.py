from sqlmodel import select

from app.database.database import SessionDep
from app.database.models import Usuario
from app.database.schemas import UsuarioCreate
from app.utils.auth_utils import get_password_hash


def get_usuarios(db: SessionDep) -> list[Usuario]:
    return db.exec(select(Usuario)).all()


def get_usuario(db: SessionDep, usuario_id: int) -> Usuario:
    return db.exec((Usuario).filter(Usuario.id == usuario_id)).first()


def get_usuario_by_email(db: SessionDep, email: str) -> Usuario:
    return db.exec(select(Usuario).filter(Usuario.email == email)).first()


def post_usuario(db: SessionDep, usuario: UsuarioCreate) -> Usuario:
    db_usuario = Usuario(
        email=str(usuario.email),
        nome=usuario.nome,
        senha=get_password_hash(usuario.senha),
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def delete_usuario(db: SessionDep, usuario_id: int) -> None:
    db_usuario = db.exec(select(Usuario).filter(Usuario.id == usuario_id)).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
