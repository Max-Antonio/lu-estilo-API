from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from typing import Annotated
from app.database.schemas import Token
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.services.auth_services import autenticar_usuario, create_access_token
from app.database.database import get_db

auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@auth_router.post('/token')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    usuario = autenticar_usuario(form_data.username, form_data.password, db)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=1440)
    access_token = create_access_token(
        data={"sub": usuario.email}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")