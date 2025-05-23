from datetime import date, datetime

from pydantic import BaseModel, EmailStr

from app.database.models import Usuario

# ------------------------------------------------------------------------------------------------
# Token


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    refresh_token: str


# ------------------------------------------------------------------------------------------------
# Usuario


class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioPublic(UsuarioBase):
    id: int

    class Config:
        from_attributes = True


# ------------------------------------------------------------------------------------------------
# Administrador


class AdministradorBase(BaseModel):
    cpf: str


class AdministradorCreate(AdministradorBase, UsuarioCreate):
    pass


class AdministradorPublic(AdministradorBase):
    id: int
    usuario: 'Usuario'


# ------------------------------------------------------------------------------------------------
# Cliente


class ClienteBase(BaseModel):
    cpf: str
    telefone: str | None = None
    endereco: str | None = None
    data_nascimento: date | None = None
    data_criacao: datetime


class ClienteCreate(ClienteBase, UsuarioCreate):
    pass


class ClienteUpdate(BaseModel):
    telefone: str | None = None
    endereco: str | None = None

    class Config:
        from_attributes = True


class ClientePublic(ClienteBase):
    id: int
    usuario: 'Usuario'
