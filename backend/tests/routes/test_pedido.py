from fastapi.testclient import TestClient
from sqlmodel import Session

from app.database.enums import PedidoStatus
from tests.utils import (
    create_cliente,
    create_pedido,
    create_produto,
    create_usuario,
    get_header_with_token,
)


def test_pedido_list(client: TestClient, session: Session):
    usuario = create_usuario()
    cliente = create_cliente(usuario)
    produtos1 = [create_produto() for _ in range(5)]
    produtos2 = [create_produto() for _ in range(10)]
    produtos3 = [create_produto() for _ in range(15)]

    session.add_all(produtos1)
    session.add_all(produtos2)
    session.add_all(produtos3)
    session.add(cliente)

    session.commit()

    pedido1 = create_pedido(produtos1, cliente)
    pedido2 = create_pedido(produtos2, cliente)
    pedido3 = create_pedido(produtos3, cliente)

    session.add(pedido1)
    session.add(pedido2)
    session.add(pedido3)
    session.commit()

    response = client.get(
        '/orders/',
        headers=get_header_with_token(usuario, client),
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 3

    for i in range(3):
        assert data[i]['id'] is not None
        assert data[i]['cliente_id'] is not None
        assert data[i]['status'] is not None
        assert data[i]['data_inicio'] is not None


def test_pedido_list_paginacao(client: TestClient, session: Session):
    usuario = create_usuario()
    cliente = create_cliente(usuario)
    produtos1 = [create_produto() for _ in range(5)]
    produtos2 = [create_produto() for _ in range(10)]
    produtos3 = [create_produto() for _ in range(15)]

    session.add_all(produtos1)
    session.add_all(produtos2)
    session.add_all(produtos3)
    session.add(cliente)

    session.commit()

    pedido1 = create_pedido(produtos1, cliente)
    pedido2 = create_pedido(produtos2, cliente)
    pedido3 = create_pedido(produtos3, cliente)

    session.add(pedido1)
    session.add(pedido2)
    session.add(pedido3)
    session.commit()

    params = {
        'skip': 0,
        'limit': 2,
    }

    response = client.get(
        '/orders/',
        headers=get_header_with_token(usuario, client),
        params=params,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    assert data[0]['id'] == 1
    assert data[1]['id'] == 2


def test_pedido_list_filtro(client: TestClient, session: Session):
    usuario = create_usuario()
    cliente = create_cliente(usuario)
    produtos1 = [create_produto(secao='feminina') for _ in range(5)]
    produtos2 = [create_produto(secao='masculina') for _ in range(10)]
    produtos3 = [create_produto(secao='feminina') for _ in range(15)]

    session.add_all(produtos1)
    session.add_all(produtos2)
    session.add_all(produtos3)
    session.add(cliente)

    session.commit()

    pedido1 = create_pedido(produtos1, cliente)
    pedido2 = create_pedido(produtos2, cliente)
    pedido3 = create_pedido(produtos3, cliente)

    session.add(pedido1)
    session.add(pedido2)
    session.add(pedido3)
    session.commit()

    params = {
        'secao_produtos': 'masculina',
    }

    response = client.get(
        '/orders/',
        headers=get_header_with_token(usuario, client),
        params=params,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    assert data[0]['id'] == 2


def test_pedido_post(client: TestClient, session: Session):
    usuario = create_usuario()
    cliente = create_cliente(usuario)
    produtos = [create_produto() for _ in range(10)]

    session.add(cliente)
    session.add_all(produtos)
    session.commit()

    produtos_id = [produto.id for produto in produtos]

    body = {
        'cliente_id': 1,
        'status': 'pedido criado, mas não confirmado pelo cliente',
        'data_inicio': '2025-01-10',
        'data_fim': '2025-05-25',
        'produtos_id': produtos_id,
    }

    response = client.post(
        '/orders/',
        headers=get_header_with_token(usuario, client),
        json=body,
    )

    assert response.status_code == 200

    data = response.json()

    assert data['id'] == 1
    assert data['cliente_id'] == 1
    assert data['status'] == 'pedido criado, mas não confirmado pelo cliente'
    assert data['data_inicio'] == '2025-01-10'
    assert data['data_fim'] == '2025-05-25'


def test_pedido_get(client: TestClient, session: Session):
    usuario = create_usuario()
    cliente = create_cliente(usuario)
    produtos1 = [create_produto() for _ in range(5)]
    produtos2 = [create_produto() for _ in range(10)]
    produtos3 = [create_produto() for _ in range(15)]

    session.add_all(produtos1)
    session.add_all(produtos2)
    session.add_all(produtos3)
    session.add(cliente)

    session.commit()

    pedido1 = create_pedido(produtos1, cliente)
    pedido2 = create_pedido(produtos2, cliente)
    pedido3 = create_pedido(produtos3, cliente)

    session.add(pedido1)
    session.add(pedido2)
    session.add(pedido3)
    session.commit()

    response = client.get(
        '/orders/2',
        headers=get_header_with_token(usuario, client),
    )

    assert response.status_code == 200

    data = response.json()

    assert data['id'] == 2


def test_pedido_update(client: TestClient, session: Session):
    usuario = create_usuario()
    cliente = create_cliente(usuario)
    produtos = [create_produto() for _ in range(5)]

    session.add_all(produtos)
    session.add(cliente)
    session.commit()

    pedido = create_pedido(produtos, cliente, PedidoStatus.confirmado)

    session.add(pedido)
    session.commit()

    body = {
        'cliente_id': cliente.id,
        'status': PedidoStatus.entregue,
    }

    response = client.put(
        '/orders/1',
        headers=get_header_with_token(usuario, client),
        json=body,
    )

    assert response.status_code == 200

    data = response.json()

    assert data['status'] == PedidoStatus.entregue


def test_pedido_delete(client: TestClient, session: Session):
    usuario = create_usuario()
    cliente = create_cliente(usuario)
    produtos = [create_produto() for _ in range(5)]

    session.add_all(produtos)
    session.add(cliente)
    session.commit()

    pedido = create_pedido(produtos, cliente)

    session.add(pedido)
    session.commit()

    response = client.delete(
        '/orders/1',
        headers=get_header_with_token(usuario, client),
    )

    assert response.status_code == 200

    data = response.json()

    assert data['detail'] == 'Pedido deletado com sucesso'
