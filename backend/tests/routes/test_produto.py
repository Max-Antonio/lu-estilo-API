from fastapi.testclient import TestClient
from sqlmodel import Session

from tests.utils import create_produto, create_usuario, get_header_with_token


def test_produto_list(client: TestClient, session: Session):
    usuario = create_usuario('olivia@email.com')
    session.add(usuario)

    produto1 = create_produto()
    produto2 = create_produto()
    produto3 = create_produto()
    produto4 = create_produto()
    session.add(produto1)
    session.add(produto2)
    session.add(produto3)
    session.add(produto4)

    session.commit()

    response = client.get(
        '/products/',
        headers=get_header_with_token(usuario, client),
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 4

    for i in range(4):
        assert data[i]['categoria'] is not None
        assert data[i]['preco'] is not None
        assert data[i]['disponivel'] is not None
        assert data[i]['id'] is not None


def test_produto_list_paginacao(client: TestClient, session: Session):
    """Testa a paginacao da rota produto_list."""
    usuario = create_usuario('aldo@email.com')
    session.add(usuario)

    produto1 = create_produto()
    produto2 = create_produto()
    produto3 = create_produto()
    produto4 = create_produto()
    session.add(produto1)
    session.add(produto2)
    session.add(produto3)
    session.add(produto4)

    session.commit()

    params = {
        'skip': 1,
        'limit': 2,
    }

    response = client.get(
        '/products/',
        headers=get_header_with_token(usuario, client),
        params=params,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    assert data[0]['id'] == 2
    assert data[1]['id'] == 3


def test_produto_list_filtro(client: TestClient, session: Session):
    """Testa os filtros da rota produto_list."""
    usuario = create_usuario('lorem@email.com')
    session.add(usuario)

    produto1 = create_produto(categoria='camisa')
    produto2 = create_produto(categoria='saia')
    produto3 = create_produto(categoria='jaqueta')
    produto4 = create_produto(categoria='jaqueta')
    session.add(produto1)
    session.add(produto2)
    session.add(produto3)
    session.add(produto4)

    session.commit()

    params = {
        'categoria': 'jaqueta',
    }

    response = client.get(
        '/products/',
        headers=get_header_with_token(usuario, client),
        params=params,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    assert data[0]['id'] == 3
    assert data[0]['categoria'] == 'jaqueta'

    assert data[1]['id'] == 4
    assert data[1]['categoria'] == 'jaqueta'


def test_produto_post(client: TestClient, session: Session):
    usuario = create_usuario('turing@email.com')
    session.add(usuario)
    session.commit()

    body = {
        'categoria': 'top',
        'preco': 16.99,
        'disponivel': True,
    }

    response = client.post(
        '/products/',
        headers=get_header_with_token(usuario, client),
        json=body,
    )

    assert response.status_code == 200

    data = response.json()

    assert data['categoria'] == 'top'
    assert data['preco'] == 16.99
    assert data['disponivel'] is True

def test_produto_get(client: TestClient, session: Session):
    usuario = create_usuario('joao@email.com')
    session.add(usuario)
    session.commit()

    produto1 = create_produto(categoria='agasalho', preco=300.99)
    produto2 = create_produto(categoria='cinto', preco=20.0)
    produto3 = create_produto(categoria='meia', preco=8.59)
    produto4 = create_produto(categoria='luva', preco=5.0)
    session.add(produto1)
    session.add(produto2)
    session.add(produto3)
    session.add(produto4)

    response = client.get(
        '/products/3',
        headers=get_header_with_token(usuario, client),
    )

    assert response.status_code == 200

    data = response.json()

    assert data['id'] == 3
    assert data['categoria'] == 'meia'
    assert data['preco'] == 8.59


def test_produto_update(client: TestClient, session: Session):
    usuario = create_usuario('jorge@email.com')
    session.add(usuario)
    session.commit()

    produto = create_produto(categoria='casaco', preco=210.89, disponivel=True)
    session.add(produto)
    session.commit()

    body = {
        'categoria': 'boina',
        'preco': 18.10,
        'disponivel': False,
    }

    response = client.put(
        '/products/1',
        headers=get_header_with_token(usuario, client),
        json=body,
    )

    assert response.status_code == 200

    data = response.json()

    #campos atualizados
    assert data['categoria'] == 'boina'
    assert data['preco'] == 18.10
    assert data['disponivel'] is False


def test_produto_delete(client: TestClient, session: Session):
    usuario = create_usuario('joanna@email.com')
    session.add(usuario)

    produto = create_produto(categoria='casaco', preco=122.89, disponivel=True)
    session.add(produto)
    session.commit()

    response = client.delete(
        '/products/1',
        headers=get_header_with_token(usuario, client),
    )

    assert response.status_code == 200

    data = response.json()

    assert data['detail'] == 'Produto deletado com sucesso'
