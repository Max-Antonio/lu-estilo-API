import secrets

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Classe que representa a configuração baseada em ambiente da API.

    As variaveis de ambiente do env são representadas pelas variáveis dessa classe.

    """

    model_config = SettingsConfigDict(env_file='.env', env_ignore_empty=True, extra='ignore')

    # Database
    DATABASE_URL: str = 'sqlite://'
    BASE_URL: str = 'http://localhost:8000'

    # Auth
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = 'HS256'


settings = Settings()
