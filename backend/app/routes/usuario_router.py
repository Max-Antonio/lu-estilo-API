from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.database.database import SessionDep
from app.database.models import Usuario
from app.database.schemas import UsuarioPublic
from app.services.auth_services import get_current_usuario_ativo
from app.services.usuario_services import delete_usuario, get_usuario, get_usuarios

usuario_router = APIRouter(tags=['Usuarios'])


@usuario_router.get('/')
def usuarios_list(db: SessionDep) -> list[UsuarioPublic]:
    return get_usuarios(db)


@usuario_router.get('/me')
def usuario_list(
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> UsuarioPublic:
    return current_usuario


@usuario_router.get('/{usuario_id}')
def usuario_info(usuario_id: int, db: SessionDep) -> UsuarioPublic:
    db_usuario = get_usuario(db, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='usuario não encontrado')
    return db_usuario


@usuario_router.delete('/{usuario_id}')
def usuario_delete(usuario_id: int, db: SessionDep):
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='usuario não encontrado')

    delete_usuario(db, db_usuario.id)
    return {'message': 'usuario deleted'}
