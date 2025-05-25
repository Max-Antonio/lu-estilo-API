from datetime import date

from sqlmodel import select

from app.database.database import SessionDep
from app.database.enums import PedidoStatus
from app.database.models import Pedido, PedidoProduto, Produto
from app.database.schemas import PedidoCreate, PedidoUpdate


def get_pedidos(
    db: SessionDep,
    skip: int,
    limit: int,
    data_inicio: date,
    data_fim: date,
    secao_produtos: str,
    pedido_id: int,
    pedido_status: PedidoStatus,
    cliente_id: PedidoStatus,
) -> list[Pedido]:
    stmt = select(Pedido)
    if data_inicio:
        stmt = stmt.where(Pedido.data_inicio >= data_inicio)
    if data_fim:
        stmt = stmt.where(Pedido.data_fim <= data_fim)
    if secao_produtos:
        stmt = (
            stmt.join(PedidoProduto, Pedido.id == PedidoProduto.pedido_id)
            .join(Produto, PedidoProduto.produto_id == Produto.id)
            .where(Produto.secao == secao_produtos)
            .distinct()
        )
    if pedido_id:
        stmt = stmt.filter(Pedido.id == pedido_id)
    if pedido_status:
        stmt = stmt.filter(Pedido.status == pedido_status)
    if cliente_id:
        stmt = stmt.filter(Pedido.cliente_id == cliente_id)

    pedidos = db.exec(stmt.offset(skip).limit(limit))

    return pedidos

def get_pedido(db: SessionDep, pedido_id: int) -> Pedido:
    return db.exec(select(Pedido).filter(Pedido.id == pedido_id)).first()

def post_pedido(db: SessionDep, pedido_data: PedidoCreate) -> Pedido:
    db_pedido = Pedido.model_validate(pedido_data)
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def update_pedido(db: SessionDep, pedido_data: PedidoUpdate, pedido: Pedido) -> Pedido:
    for key, value in pedido_data.model_dump(exclude_unset=True).items():
        setattr(pedido, key, value)

    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    return pedido