from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.database.enums import PedidoStatus, Role
from app.database.models import Cliente, Produto, Usuario

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
    role: Role


class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioPublic(UsuarioBase):
    id: int

    model_config = ConfigDict(from_attributes = True)


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

    model_config = ConfigDict(from_attributes = True)


class ClientePublic(ClienteBase):
    id: int
    usuario: 'Usuario'


# ------------------------------------------------------------------------------------------------
# Produto


class ProdutoBase(BaseModel):
    categoria: str
    secao: str
    preco: float
    disponivel: bool


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(ProdutoBase):
    model_config = ConfigDict(from_attributes = True)


class ProdutoPublic(ProdutoBase):
    id: int

# ------------------------------------------------------------------------------------------------
# Pedido

class PedidoBase(BaseModel):
    cliente_id: int
    status: PedidoStatus | None = None
    data_inicio: date | None = None
    data_fim:  date | None = None

class PedidoCreate(PedidoBase):
    produtos_id: list[int]

class PedidoUpdate(PedidoBase):
    pass

class PedidoPublic(PedidoBase):
    id: int
    cliente: 'Cliente'
    produtos: list['Produto']
