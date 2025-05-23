from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.database.database import SessionDep
from app.database.models import Usuario
from app.database.schemas import ClienteCreate, ClientePublic, ClienteUpdate
from app.services.auth_services import get_current_usuario_ativo
from app.services.cliente_services import (
    get_cliente,
    get_clientes,
    post_cliente,
    update_cliente,
)
from app.services.usuario_services import get_usuario_by_email, post_usuario

cliente_router = APIRouter(tags=['Clientes'])


@cliente_router.get('/')
def cliente_list(
    *,
    skip: int = 0,
    limit: int | None = None,
    nome: Annotated[str | None, Query(description='Filtro por nome')] = None,
    email: Annotated[str | None, Query(description='Filtro por email')] = None,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> list[ClientePublic]:
    return get_clientes(db, skip, limit, nome, email)


@cliente_router.post('/')
def cliente_post(
    cliente_data: ClienteCreate,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> ClientePublic:
    usuario_existente = get_usuario_by_email(db, cliente_data.email)
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='email já utilizado',
        )

    usuario = post_usuario(db, cliente_data)

    cliente = post_cliente(db, usuario.id, cliente_data)

    return cliente


@cliente_router.get('/{id}')
def cliente_get(
    id: int,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> ClientePublic:
    cliente = get_cliente(db, id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='cliente não encontrado',
        )

    return cliente


@cliente_router.put('/{id}')
def cliente_put(
    id: int,
    cliente_data: ClienteUpdate,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> ClientePublic:
    cliente = get_cliente(db, id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='cliente não encontrado',
        )

    cliente_update = update_cliente(db, cliente_data, cliente)

    return cliente_update


@cliente_router.delete('/{id}')
def cliente_delete(
    id: int,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> None:
    cliente = get_cliente(db, id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='cliente não encontrado',
        )

    db.delete(cliente)
    db.commit()

    return {'detail': 'Cliente deletado com sucesso'}
