from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.services.auth_services import get_current_usuario_ativo
from app.database.database import get_db
from app.database.models import Usuario
from app.database.schemas import UsuarioSchema, UsuarioCreate
from app.services.usuario_services import get_usuarios, create_usuario, get_usuario, delete_usuario

usuario_router = APIRouter(
    prefix='/usuarios',
    tags=['Usuarios']
)


@usuario_router.get('/', response_model=list[UsuarioSchema])
def usuario_list(db: Session = Depends(get_db)):
    db_usuarios = get_usuarios(db)

    return db_usuarios


@usuario_router.get('/me', response_model=UsuarioSchema)
def usuario_list(current_usuario: Usuario = Depends(get_current_usuario_ativo)):
    return current_usuario


@usuario_router.get('/{usuario_id}', response_model=UsuarioSchema)
def usuario_info(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = get_usuario(db, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="usuario não encontrado")
    return db_usuario


@usuario_router.delete('/{usuario_id}')
def usuario_delete(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="usuario não encontrado")

    delete_usuario(db, db_usuario.id)
    return {"message": "usuario deleted"}


@usuario_router.post("/", response_model=UsuarioSchema)
def usuario_post(usuario: UsuarioCreate, db:Session = Depends(get_db)):
    return create_usuario(db, usuario)