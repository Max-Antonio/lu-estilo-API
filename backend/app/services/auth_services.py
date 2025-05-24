from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from app.config import settings
from app.database.database import SessionDep
from app.database.enums import Role
from app.database.models import Usuario
from app.database.schemas import TokenData
from app.services.usuario_services import get_usuario_by_email
from app.utils.auth_utils import verify_password

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Não foi possível validar as credenciais, faça o login novamente.',
    headers={'WWW-Authenticate': 'Bearer'},
)


def autenticar_usuario(email: str, senha: str, db: SessionDep) -> Usuario:
    usuario = get_usuario_by_email(db, email)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='usuario não encontrado')
    if not verify_password(senha, usuario.senha):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='senha incorreta')
    return usuario


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode = data.copy()
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_usuario(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: SessionDep,
) -> Usuario:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('sub')
        if not email:
            raise credentials_exception
        token_data = TokenData(email=email)
    except (jwt.InvalidTokenError, ValidationError):
        raise credentials_exception
    usuario = get_usuario_by_email(db, email=token_data.email)
    if not usuario:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Usuario não encontrado')
    return usuario


async def get_current_usuario_ativo(
    current_user: Usuario = Depends(get_current_usuario),
) -> Usuario:
    return current_user


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None

def valida_admin(usuario: Usuario) -> None:
    if usuario.role != Role.ADMIN:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Usuário não autorizado a usar esta rota')