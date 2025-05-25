from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.database.database import SessionDep
from app.database.models import Usuario
from app.database.schemas import ClienteCreate, ClientePublic, ClienteUpdate
from app.services.auth_services import get_current_usuario_ativo, valida_admin
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
    """Lista os clientes registrados no sistema.

    Args:
    ----
        skip (int): número de itens da lista a serem pulados.
        limit (int): número limite de itens da lista a serem retornados.
        nome: (str): nome do cliente.
        email: (str): email do cliente.
        db (SessionDep): Session do banco de dados.
        current_usuario (Usuario): Usuário atual logado.

    Returns:
    -------
        list[ClientePublic]: lista com informações dos clientes.


    """
    return get_clientes(db, skip, limit, nome, email)


@cliente_router.post('/')
def cliente_post(
    cliente_data: ClienteCreate,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> ClientePublic:
    """Registra um cliente no sistema e associa um usuário ao cliente.

    Args:
    ----
        cliente_data (ClienteCreate): schema com informações do cliente.
        db (SessionDep): Session do banco de dados.
        current_usuario (Usuario): Usuário atual logado.

    Returns:
    -------
        ClienteCreate: informações do cliente registrado.

    """
    valida_admin(current_usuario)
    usuario_existente = get_usuario_by_email(db, cliente_data.email)
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='email já utilizado',
        )

    usuario = post_usuario(db, cliente_data)

    return post_cliente(db, usuario.id, cliente_data)


@cliente_router.get('/{id}')
def cliente_get(
    id: int,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> ClientePublic:
    """Pega informações de um cliente dado seu id.

    Args:
    ----
        id (int): id do cliente.
        db (SessionDep): Session do banco de dados.
        current_usuario (Usuario): Usuário atual logado.

    Returns:
    -------
        ClientePublic: informações do cliente.

    """
    cliente = get_cliente(db, id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='cliente não encontrado',
        )

    return cliente


@cliente_router.put('/{id}')
def cliente_update(
    id: int,
    cliente_data: ClienteUpdate,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> ClientePublic:
    """Atualiza informações do cliente.

    Args:
    ----
        id (int): id do cliente.
        cliente_data (int): schema com as novas informações do cliente a serem atualizadas.
        db (SessionDep): Session do banco de dados.
        current_usuario (Usuario): Usuário atual logado.

    Returns:
    -------
        ClientePublic: informações do cliente atualizadas.


    """
    valida_admin(current_usuario)
    cliente = get_cliente(db, id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='cliente não encontrado',
        )

    return update_cliente(db, cliente_data, cliente)


@cliente_router.delete('/{id}')
def cliente_delete(
    id: int,
    db: SessionDep,
    current_usuario: Annotated[Usuario, Depends(get_current_usuario_ativo)],
) -> None:
    """Deleta um cliente do sistema dado seu id.

    Args:
    ----
        id (int): id do cliente.
        db (SessionDep): Session do banco de dados.
        current_usuario (Usuario): Usuário atual logado.

    Returns:
    -------
        Mensagem de confirmação que o cliente foi deletado.

    """
    valida_admin(current_usuario)
    cliente = get_cliente(db, id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='cliente não encontrado',
        )

    db.delete(cliente)
    db.commit()

    return {'detail': 'Cliente deletado com sucesso'}
