from datetime import date, datetime
from random import choice, choices, randint
from string import ascii_letters, digits

from fastapi.testclient import TestClient
from pytz import timezone

from app.config import settings
from app.database.models import Cliente, Usuario
from app.utils.auth_utils import get_password_hash


def rand_str(len: int = 20, word_set: list[str] | None = None) -> str:
    if word_set is not None:
        return choice(word_set)

    word = ''
    for _ in range(len):
        word += choice(ascii_letters + 'çíúéá')
    return word


def rand_bool() -> bool:
    return bool(randint(0, 1))


def rand_int(a: int = 0, b: int = 50):
    return randint(a, b)


def rand_cpf() -> str:
    return ''.join(choices(digits, k=11))


def rand_email() -> str:
    return f'{rand_str()}@example.com'


def rand_date() -> date:
    return date(
        year=rand_int(2010, 2024),
        month=rand_int(1, 12),
        day=rand_int(1, 28),
    )


def rand_datetime() -> datetime:
    return datetime(
        year=rand_int(2010, 2024),
        month=rand_int(1, 12),
        day=rand_int(1, 28),
        hour=rand_int(0, 23),
        minute=rand_int(0, 59),
        second=rand_int(0, 59),
        tzinfo=timezone.utc,
    )


def create_usuario(email: str = rand_email(), senha: str | None = None):
    """Email não é randomizado para evitar a possibilidade de usuarios com o mesmo email."""
    return Usuario(
        nome=rand_str(),
        email=email,
        senha=get_password_hash(senha or settings.DEFAULT_TEST_PASSWORD),
    )


def create_cliente(usuario: Usuario, cpf: str = rand_cpf()):
    """Email não é randomizado para evitar a possibilidade de clientes com o mesmo cpf."""
    return Cliente(
        cpf=cpf,
        telefone=rand_str(),
        endereco=rand_str(),
        data_nascimento=rand_date(),
        usuario=usuario,
    )


def get_token(usuario: Usuario, client: TestClient):
    response = client.post(
        '/auth/login/',
        data={
            'username': usuario.email,
            'password': settings.DEFAULT_TEST_PASSWORD,
        },
    )
    return response.json()['access_token']


def get_header_with_token(usuario: Usuario, client: TestClient):
    token = get_token(usuario, client)
    return {
        'Authorization': f'Bearer {token}',
    }
