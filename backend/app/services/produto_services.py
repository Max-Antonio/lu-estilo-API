from sqlmodel import select

from app.database.database import SessionDep
from app.database.models import Produto
from app.database.schemas import ProdutoCreate, ProdutoPublic, ProdutoUpdate


def get_produtos(
    db: SessionDep,
    skip: int,
    limit: int,
    categoria: str | None,
    preco: float | None,
    disponivel: bool | None,
) -> list[Produto]:
    stmt = select(Produto)
    if categoria:
        stmt = stmt.filter(Produto.categoria == categoria)
    if preco:
        stmt = stmt.filter(Produto.preco == preco)
    if disponivel:
        stmt = stmt.filter(Produto.disp)

    produtos = db.exec(stmt.offset(skip).limit(limit))

    return produtos


def get_produto(db: SessionDep, produto_id: int) -> Produto:
    return db.exec(select(Produto).filter(Produto.id == produto_id)).first()


def post_produto(db: SessionDep, produto_data: ProdutoCreate) -> Produto:
    db_produto = Produto.model_validate(produto_data)
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def update_produto(db: SessionDep, produto_data: ProdutoUpdate, produto: Produto) -> Produto:
    for key, value in produto_data.model_dump(exclude_unset=True).items():
        setattr(produto, key, value)

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return produto