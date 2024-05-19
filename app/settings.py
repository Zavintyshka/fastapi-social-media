from pydantic_settings import BaseSettings, SettingsConfigDict

TEST_MODE = True


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="app/.env", env_file_encoding="UTF-8")
    DB_USER: str
    DB_PASSWORD: int
    HOST: str
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


settings = Settings()
