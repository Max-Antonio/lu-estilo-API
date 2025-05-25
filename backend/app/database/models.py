from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.database.enums import PedidoStatus, Role

# ------------------------------------------------------------------------------------------------
# Usuario


class Usuario(SQLModel, table=True):
    __tablename__ = 'usuario'

    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str
    senha: str
    role: Role = Field(default=Role.user)

    cliente: Optional['Cliente'] = Relationship(back_populates='usuario')


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

    usuario: 'Usuario' = Relationship(back_populates='cliente')
    pedidos: list['Pedido'] = Relationship(back_populates='cliente')


# ------------------------------------------------------------------------------------------------
# Produto


class PedidoProduto(SQLModel, table=True):
    """Tabela criada pela relação muitos pra muitos de Pedido e Produto.

    um produto pode estar em muitos pedidos e um pedido pode ter muitos produtos.
    """

    __tablename__ = 'pedido_produto'

    produto_id: int = Field(foreign_key='produto.id', primary_key=True, ondelete='CASCADE')
    pedido_id: int = Field(foreign_key='pedido.id', primary_key=True, ondelete='CASCADE')


class Produto(SQLModel, table=True):
    __tablename__ = 'produto'

    id: int | None = Field(default=None, primary_key=True)
    categoria: str
    secao: str
    preco: float
    disponivel: bool

    pedidos: list['Pedido'] = Relationship(
        back_populates='produtos',
        link_model=PedidoProduto,
    )


# ------------------------------------------------------------------------------------------------
# Pedido


class Pedido(SQLModel, table=True):
    __tablename__ = 'pedido'

    id: int | None = Field(default=None, primary_key=True)
    cliente_id: int = Field(index=True, foreign_key='cliente.id')
    status: PedidoStatus = Field(default=PedidoStatus.pendente)
    data_inicio: date = Field(default_factory=date.today)
    data_fim:  date | None = Field()
    cliente: 'Cliente' = Relationship(back_populates='pedidos')
    produtos: list['Produto'] = Relationship(
        back_populates='pedidos',
        link_model=PedidoProduto,
    )
