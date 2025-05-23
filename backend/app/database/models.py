from datetime import date, datetime

from sqlmodel import Field, Relationship, SQLModel

# ------------------------------------------------------------------------------------------------
# Usuario


class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str
    senha: str


# ------------------------------------------------------------------------------------------------
# Adminstrador


class Administrador(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cpf: str = Field(min_length=11, max_length=11, unique=True)
    usuario_id: int = Field(index=True, foreign_key='usuario.id')

    usuario: 'Usuario' = Relationship()


# ------------------------------------------------------------------------------------------------
# Cliente


class Cliente(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cpf: str = Field(min_length=11, max_length=11, unique=True)
    telefone: str | None = None
    endereco: str | None = None
    data_criacao: datetime = Field(default_factory=datetime.now)
    data_nascimento: date | None = None
    usuario_id: int = Field(index=True, foreign_key='usuario.id')

    usuario: 'Usuario' = Relationship()
