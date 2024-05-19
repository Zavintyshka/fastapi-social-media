from pydantic_settings import BaseSettings, SettingsConfigDict
from alembic.config import Config

alembic_cfg = Config("alembic.ini")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="tests/.env", env_file_encoding="UTF-8")
    DB_USER_TEST: str
    DB_PASSWORD_TEST: int
    HOST_TEST: str
    DB_NAME_TEST: str


settings = Settings()

