from fastapi.testclient import TestClient


def test_usuario_post(client: TestClient):
    body = {'nome': 'pedro', 'email': 'pedro@email.com', 'senha': 'senha123'}
    response = client.post('/auth/register', json=body)
    assert response.status_code == 200


def test_login_for_access_token(client: TestClient):
    body = {'nome': 'amanda', 'email': 'amanda@email.com', 'senha': 'senha321'}
    client.post('/auth/register', json=body)

    body_login = {
        'username': 'amanda@email.com',
        'password': 'senha321',
    }

    response = client.post('/auth/login', data=body_login)
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'bearer'
