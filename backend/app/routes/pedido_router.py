from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.database.database import SessionDep
from app.database.enums import PedidoStatus
from app.database.models import Usuario
from app.database.schemas import PedidoCreate, PedidoPublic, PedidoUpdate
from app.services.auth_services import get_current_usuario_ativo, valida_admin
from app.services.pedido_services import get_pedido, get_pedidos, post_pedido, update_pedido

pedido_router = APIRouter(tags=['Pedidos'])


@pedido_router.get('/')
def pedido_list(
    *,
    skip: int = 0,
    limit: int | None = None,
    data_inicio: Annotated[date | None, Query(description='Filtro por data de inicio')] = None,
    data_fim: Annotated[date | None, Query(description='Filtro por data final')] = None,
    secao_produtos: Annotated[str | None, Query(description='Filtro por seção de produtos')] = None,
    id_pedido: Annotated[int | None, Query(description='Filtro por id de pedido')] = None,
    pedido_status: Annotated[
        PedidoStatus | None,
        Query(description='Filtro por id de pedido'),
    ] = None,
    id_cliente: Annotated[
        PedidoStatus | None,
        Query(description='Filtro por id de cliente'),
    ] = None,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> list[PedidoPublic]:
    return get_pedidos(
        db,
        skip,
        limit,
        data_inicio,
        data_fim,
        secao_produtos,
        id_pedido,
        pedido_status,
        id_cliente,
    )


@pedido_router.post('/')
def pedido_post(
    pedido_data: PedidoCreate,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> PedidoPublic:
    valida_admin(current_usuario)
    return post_pedido(db, pedido_data)


@pedido_router.get('/{id}')
def pedido_get(
    id: int, db: SessionDep, current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> PedidoPublic:
    pedido = get_pedido(db, id)
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='pedido não encontrado',
        )

    return pedido


@pedido_router.put('/{id}')
def pedido_update(
    id: int,
    pedido_data: PedidoUpdate,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> PedidoPublic:
    valida_admin(current_usuario)
    pedido = get_pedido(db, id)
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='pedido não encontrado',
        )

    return update_pedido(db, pedido_data, pedido)


@pedido_router.delete('/{id}')
def pedido_delete(
    id: int, db: SessionDep, current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
):
    valida_admin(current_usuario)
    pedido = get_pedido(db, id)
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='pedido não encontrado',
        )
    db.delete(pedido)
    db.commit()

    return {'detail': 'Pedido deletado com sucesso'}
