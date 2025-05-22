from sqlalchemy.orm import Session

from app.database.models import Usuario
from app.database.schemas import UsuarioCreate
from app.utils.auth_utils import get_password_hash

def get_usuarios(db: Session):
    return db.query(Usuario).all()


def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()


def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(
        email=str(usuario.email),
        nome=usuario.nome,
        senha=get_password_hash(usuario.senha)
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def delete_usuario(db: Session, usuario_id: int):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
    return
