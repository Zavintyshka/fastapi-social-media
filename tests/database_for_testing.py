# 3rd Party
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Project's modules
from .settings import settings

SQLALCHEMY_DB_URL = f"postgresql+psycopg://{settings.DB_USER_TEST}:{settings.DB_PASSWORD_TEST}@{settings.HOST_TEST}/{settings.DB_NAME_TEST}"
SQLALCHEMY_ENGINE = create_engine(SQLALCHEMY_DB_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=SQLALCHEMY_ENGINE)

Base = declarative_base()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
