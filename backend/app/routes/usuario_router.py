from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.database.database import SessionDep
from app.database.models import Usuario
from app.database.schemas import UsuarioPublic
from app.services.auth_services import get_current_usuario_ativo
from app.services.usuario_services import get_usuario, get_usuarios

usuario_router = APIRouter(tags=['Usuarios'])


@usuario_router.get('/')
def usuarios_list(
    db: SessionDep, current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> list[UsuarioPublic]:
    """Lista os usuários registrados no sistema.

    Args:
    ----
        db (SessionDep): Session do banco de dados.
        current_usuario (Usuario): Usuário atual logado.

    Returns:
    -------
        list[UsuarioPublic]: lista com informações dos usuários.

    """
    return get_usuarios(db)


@usuario_router.get('/me')
def usuario_atual(
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> UsuarioPublic:
    """Retorna o usuário atual logado.

    Returns
    -------
        UsuarioPublic: informações do usuário atual logado

    """
    return current_usuario


@usuario_router.get('/{usuario_id}')
def usuario_get(
    usuario_id: int,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> UsuarioPublic:
    """Pega informações de um usuário dado seu id.

    Args:
    ----
        id (int): id do usuário.
        db (SessionDep): Session do banco de dados.
        current_usuario (Usuario): Usuário atual logado.

    Returns:
    -------
        UsuarioPublic: informações do usuário

    """
    db_usuario = get_usuario(db, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='usuario não encontrado')
    return db_usuario
