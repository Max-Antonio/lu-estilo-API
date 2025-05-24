from fastapi.testclient import TestClient
from sqlmodel import Session

from tests.utils import create_cliente, create_usuario, get_header_with_token


def test_cliente_list(client: TestClient, session: Session):
    usuario1 = create_usuario('ronaldo@email.com')
    usuario2 = create_usuario('jessica@email.com')
    usuario3 = create_usuario('adao@email.com')
    cliente1 = create_cliente(usuario1, '11111111111')
    cliente2 = create_cliente(usuario2, '22222222222')
    cliente3 = create_cliente(usuario3, '33333333333')
    session.add(cliente1)
    session.add(cliente2)
    session.add(cliente3)
    session.commit()

    response = client.get(
        '/clients/',
        headers=get_header_with_token(usuario1, client),
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 3
    for i in range(3):
        assert data[i]['cpf'] is not None
        assert data[i]['telefone'] is not None
        assert data[i]['endereco'] is not None
        assert data[i]['data_nascimento'] is not None
        assert data[i]['data_criacao'] is not None
        assert data[i]['id'] is not None
        assert data[i]['usuario'] is not None


def test_cliente_list_paginacao(client: TestClient, session: Session):
    usuario1 = create_usuario('ronaldo@email.com')
    usuario2 = create_usuario('jessica@email.com')
    usuario3 = create_usuario('adao@email.com')
    usuario4 = create_usuario('ofelia@email.com')
    usuario5 = create_usuario('genildo@email.com')
    cliente1 = create_cliente(usuario1, '11111111111')
    cliente2 = create_cliente(usuario2, '22222222222')
    cliente3 = create_cliente(usuario3, '33333333333')
    cliente4 = create_cliente(usuario4, '44444444444')
    cliente5 = create_cliente(usuario5, '55555555555')
    session.add(cliente1)
    session.add(cliente2)
    session.add(cliente3)
    session.add(cliente4)
    session.add(cliente5)
    session.commit()

    params = {
        'skip': 1,
        'limit': 2,
    }

    response = client.get(
        '/clients/',
        headers=get_header_with_token(usuario1, client),
        params=params,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    assert data[0]['cpf'] == '22222222222'
    assert data[1]['cpf'] == '33333333333'


def test_cliente_list_filtro(client: TestClient, session: Session):
    usuario1 = create_usuario('ronaldo@email.com')
    usuario2 = create_usuario('jessica@email.com')
    usuario3 = create_usuario('adao@email.com')
    cliente1 = create_cliente(usuario1, '11111111111')
    cliente2 = create_cliente(usuario2, '22222222222')
    cliente3 = create_cliente(usuario3, '33333333333')
    session.add(cliente1)
    session.add(cliente2)
    session.add(cliente3)
    session.commit()

    params = {
        'email': 'ronaldo@email.com',
    }

    response = client.get(
        '/clients/',
        headers=get_header_with_token(usuario1, client),
        params=params,
    )

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1

    assert data[0]['cpf'] == '11111111111'


def test_client_post(client: TestClient, session: Session):
    usuario = create_usuario('alex@email.com')
    session.add(usuario)
    session.commit()

    body = {
        'nome': 'arnaldo',
        'email': 'arnaldo@example.com',
        'senha': '10921090',
        'cpf': '66666666666',
        'telefone': '11111111111',
        'endereco': 'rua 8',
        'data_nascimento': '2025-05-23',
        'data_criacao': '2025-05-23T21:06:53.513Z',
    }

    response = client.post(
        '/clients/',
        headers=get_header_with_token(usuario, client),
        json=body,
    )

    assert response.status_code == 200

    data = response.json()

    assert data['usuario']['nome'] == 'arnaldo'
    assert data['usuario']['email'] == 'arnaldo@example.com'
    assert data['usuario']['senha'] is not None
    assert data['cpf'] == '66666666666'
    assert data['telefone'] == '11111111111'
    assert data['endereco'] == 'rua 8'
    assert data['data_nascimento'] == '2025-05-23'
    assert data['data_criacao'] is not None


def test_cliente_get(client: TestClient, session: Session):
    usuario1 = create_usuario('leila@email.com')
    usuario2 = create_usuario('sonia@email.com')
    usuario3 = create_usuario('robson@email.com')
    cliente1 = create_cliente(usuario1, '11111111111')
    cliente2 = create_cliente(usuario2, '22222222222')
    cliente3 = create_cliente(usuario3, '33333333333')
    session.add(cliente1)
    session.add(cliente2)
    session.add(cliente3)
    session.commit()

    response = client.get(
        '/clients/2',
        headers=get_header_with_token(usuario3, client),
    )

    assert response.status_code == 200

    data = response.json()

    assert data['usuario']['nome'] is not None
    assert data['usuario']['email'] == 'sonia@email.com'
    assert data['usuario']['senha'] is not None
    assert data['cpf'] == '22222222222'
    assert data['telefone'] is not None
    assert data['endereco'] is not None
    assert data['data_nascimento'] is not None
    assert data['data_criacao'] is not None


def test_cliente_update(client: TestClient, session: Session):
    usuario = create_usuario('breno@email.com')
    cliente = create_cliente(usuario, '23232323232')
    session.add(cliente)
    session.commit()

    body = {
            'nome': 'arnaldo',
            'email': 'arnaldo@example.com',
            'senha': '10921090',
            'cpf': '66666666666',
            'telefone': '11111111111',
            'endereco': 'rua A',
            'data_nascimento': '2000-01-20',
            'data_criacao': '2022-05-23T21:06:53.513Z',
        }

    client.post(
        '/clients/',
        headers=get_header_with_token(usuario, client),
        json=body,
    )

    body_update = {
        'endereco': 'rua Z',
        'telefone': '77777777777',
    }

    response = client.put(
        '/clients/2',
        headers=get_header_with_token(usuario, client),
        json=body_update,
    )

    assert response.status_code == 200

    data = response.json()

    # campos atualizados
    assert data['endereco'] == 'rua Z'
    assert data['telefone'] == '77777777777'

    assert data['usuario']['nome'] == 'arnaldo'
    assert data['usuario']['email'] == 'arnaldo@example.com'
    assert data['usuario']['senha'] is not None
    assert data['cpf'] == '66666666666'
    assert data['data_nascimento'] == '2000-01-20'
    assert data['data_criacao'] is not None

def test_cliente_delete(client: TestClient, session: Session):
    usuario = create_usuario('felipe@email.com')
    cliente = create_cliente(usuario, '8888888888')
    session.add(cliente)
    session.commit()

    response = client.delete(
        '/clients/1',
        headers=get_header_with_token(usuario, client),
    )

    assert response.status_code == 200

    data = response.json()

    assert data['detail'] == 'Cliente deletado com sucesso'
