# Backend Lu Estilo API

## Configurando

O Poetry é uma ferramenta intuitiva para gerenciamento de dependências e configuração de
ferramentas. Ele é controlado via `pyproject.toml`. [Como instalar](https://python-poetry.org/docs/#installing-with-pipx).

Uma rota já está configurada no módulo `app`. Para executá-la execute os seguintes comandos no terminal:
```sh
# Cria e instala as dependências num venv local.
$ poetry install
# Executa comandos no venv.
$ poetry run uvicorn app.main:app --reload
```
## testes

Para executar os testes basta executar o comando pytest na pasta backend.
```sh
# Testar todas as rotas.
$ pytest
# Testar uma rota específica
$ pytest tests/routes/test_cliente.py

```

## Deploy

Use o docker para buildar a imagem.

```sh
$ docker build -t luestilo .
```

Depois rode um cointeiner baseado na imagem.

```sh
$ docker run -d -p 8000:8000 luestilo
```