FROM python:3.12-slim

RUN apt-get update && apt-get install -y libpq-dev gcc

# Instala o Poetry
RUN pip install poetry

# diretorio
WORKDIR /app

# Copia pyproject.toml e poetry.lock
COPY pyproject.toml poetry.lock ./

# Instala as dependencias
RUN poetry config virtualenvs.create false \
    && poetry install

# Copia código da aplicação
COPY . .

# port
EXPOSE 8000

# roda com poetry
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]