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
    categoria: Annotated[str | None, Query(description='Filtro por nome')] = None,
    preco: Annotated[float | None, Query(description='Filtro por nome')] = None,
    disponivel: Annotated[bool | None, Query(description='Filtro por email')] = None,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> list[ProdutoPublic]:
    return get_produtos(db, skip, limit, categoria, preco, disponivel)


@produto_router.post('/')
def produto_post(
    produto_data: ProdutoCreate,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> ProdutoPublic:
    valida_admin(current_usuario)
    produto = post_produto(db, produto_data)
    return produto


@produto_router.get('/{id}')
def produto_get(
    id: int, db: SessionDep, current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> ProdutoPublic:
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
    valida_admin(current_usuario)
    produto = get_produto(db, id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='produto não encontrado',
        )

    produto_new = update_produto(db, produto_data, produto)

    return produto_new


@produto_router.delete('/{id}')
def produto_delete(id: int,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)]) -> None:
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

