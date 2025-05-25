from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.database.database import SessionDep
from app.database.models import Usuario
from app.database.schemas import ProdutoCreate, ProdutoPublic, ProdutoUpdate
from app.services.auth_services import get_current_usuario_ativo, valida_admin
from app.services.produto_services import get_produto, get_produtos, post_produto, update_produto

produto_router = APIRouter(tags=['Produtos'])


@produto_router.get('/')
def produto_list(
    *,
    skip: int = 0,
    limit: int | None = None,
    categoria: Annotated[str | None, Query(description='Filtro por categoria')] = None,
    preco: Annotated[float | None, Query(description='Filtro por preco')] = None,
    disponivel: Annotated[bool | None, Query(description='Filtro por disponibilidade')] = None,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> list[ProdutoPublic]:
    """Lista os produtos registrados no sistema.

    Args:
    ----
        skip (int): número de itens da lista a serem pulados.
        limit (int): número limite de itens da lista a serem retornados.
        categoria (str): categoria do produto (camisa, agasalho, meia etc.)
        preco (int): preco do produto.
        disponivel (bool): disponibilidade do produto.
        db (SessionDep): Session do banco de dados.
        current_usuario (Usuario): Usuário atual logado.

    Returns:
    -------
        list[ProdutoPublic]: lista com informações dos produtos.

    """
    return get_produtos(db, skip, limit, categoria, preco, disponivel)


@produto_router.post('/')
def produto_post(
    produto_data: ProdutoCreate,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> ProdutoPublic:
    """Registra um produto no sistema.

    Args:
    ----
        produto_data (ProdutoCreate): schema com informações do produto.
        db (SessionDep): Session do banco de dados.
        current_usuario (Usuario): Usuário atual logado.

    Returns:
    -------
        ProdutoCreate: informações do produto registrado.

    """
    valida_admin(current_usuario)
    return post_produto(db, produto_data)


@produto_router.get('/{id}')
def produto_get(
    id: int, db: SessionDep, current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> ProdutoPublic:
    """Pega informações de um produto dado seu id.

    Args:
    ----
        id (int): id do produto.
        db (SessionDep): Session do banco de dados.
        current_usuario (Usuario): Usuário atual logado.

    Returns:
    -------
        ProdutoPublic: informações do produto

    """
    produto = get_produto(db, id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='produto não encontrado',
        )

    return produto


@produto_router.put('/{id}')
def produto_update(
    id: int,
    produto_data: ProdutoUpdate,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> ProdutoPublic:
    """Atualiza informações do produto.

    Args:
    ----
        id (int): id do produto.
        pedido_data (int): schema com as novas informações do produto a serem atualizadas.
        db (SessionDep): Session do banco de dados.
        current_usuario (Usuario): Usuário atual logado.

    Returns:
    -------
        ProdutoPublic: informações do produto atualizadas

    """
    valida_admin(current_usuario)
    produto = get_produto(db, id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='produto não encontrado',
        )

    return update_produto(db, produto_data, produto)


@produto_router.delete('/{id}')
def produto_delete(id: int,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)]) -> None:
    """Deleta um produto do sistema dado seu id.

    Args:
    ----
        id (int): id do produto.
        db (SessionDep): Session do banco de dados.
        current_usuario (Usuario): Usuário atual logado.

    Returns:
    -------
        Mensagem de confirmação que o produto foi deletado

    """
    valida_admin(current_usuario)
    produto = get_produto(db, id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='produto não encontrado',
        )

    db.delete(produto)
    db.commit()

    return {'detail': 'Produto deletado com sucesso'}

