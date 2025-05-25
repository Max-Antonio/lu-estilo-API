from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.database.database import SessionDep
from app.database.schemas import (
    Token,
    TokenRefreshRequest,
    TokenResponse,
    UsuarioCreate,
    UsuarioPublic,
)
from app.services.auth_services import (
    autenticar_usuario,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.services.usuario_services import post_usuario

auth_router = APIRouter(
    tags=['Auth'],
)


@auth_router.post('/login')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: SessionDep,
) -> Token:
    """Retorna o token de autenticação.

    Args:
    ----
        form_data (OAuth2PasswordRequestForm): formulário de login com email e senha
        db (SessionDep): Session do banco de dados.

    Returns:
    -------
        Token: token de autenticação

    """
    usuario = autenticar_usuario(form_data.username, form_data.password, db)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Email ou senha incorretos',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=1440)
    access_token = create_access_token(
        data={'sub': usuario.email},
        expires_delta=access_token_expires,
    )

    return Token(access_token=access_token, token_type='bearer')


@auth_router.post('/register')
def usuario_post(usuario: UsuarioCreate, db: SessionDep) -> UsuarioPublic:
    """Registra um usuário no sistema.

    Args:
    ----
        usuario (UsuarioCreate): schema com as informações do usuário
        db (SessionDep): Session do banco de dados

    Returns:
    -------
        UsuarioPublic: informações do usuário registrado

    """
    return post_usuario(db, usuario)


@auth_router.post('/refresh-token')
def refresh_token(token_data: TokenRefreshRequest) -> TokenResponse:
    """Retorna o refreshed token.

    Args:
    ----
        token_data (TokenRefreshRequest): Requisição do refresh de Token.

    Returns:
    -------
        Token: token de autenticação refreshed

    """
    payload = verify_token(token_data.refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token inválido',
        )

    user_id = payload.get('sub')
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token payload inválido',
        )

    new_access_token = create_access_token({'sub': user_id})
    new_refresh_token = create_refresh_token({'sub': user_id})

    return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)
