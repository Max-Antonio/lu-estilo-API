from datetime import date, datetime

from sqlmodel import Field, Relationship, SQLModel

from app.database.enums import Role

# ------------------------------------------------------------------------------------------------
# Usuario


class Usuario(SQLModel, table=True):
    __tablename__ = 'usuario'

    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str
    senha: str
    role: Role = Field(default='user')

# ------------------------------------------------------------------------------------------------
# Cliente


class Cliente(SQLModel, table=True):
    __tablename__ = 'cliente'

    id: int | None = Field(default=None, primary_key=True)
    cpf: str = Field(min_length=11, max_length=11, unique=True)
    telefone: str | None = None
    endereco: str | None = None
    data_criacao: datetime = Field(default_factory=datetime.now)
    data_nascimento: date | None = None
    usuario_id: int = Field(index=True, foreign_key='usuario.id')

    usuario: 'Usuario' = Relationship()

# ------------------------------------------------------------------------------------------------
# Produto

class Produto(SQLModel, table=True):
    __tablename__ = 'produto'

    id: int | None = Field(default=None, primary_key=True)
    categoria: str
    preco: float
    disponivel: bool