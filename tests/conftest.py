import pytest
from fastapi.testclient import TestClient
from requests import Response

from app.start_server import app
from app.database import get_db
from app.schemas import Token
from .database_for_testing import TestingSessionLocal
from .data_for_testing import USER_DATA, USER_DATA2, POST1, POST2, POST3


@pytest.fixture
def session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def create_first_user(client):
    client.post("/users/", json=USER_DATA)


@pytest.fixture
def create_second_user(client):
    client.post("/users/", json=USER_DATA2)


@pytest.fixture
def first_user_authentication_header(create_first_user, client):
    user_credentials = {"username": USER_DATA["email"], "password": USER_DATA["password"]}
    response: Response = client.post("/login/", data=user_credentials)
    token = Token(**response.json())
    return {"Authorization": f"Bearer {token.access_token}"}


@pytest.fixture
def second_user_authentication_header(create_second_user, client):
    user_credentials = {"username": USER_DATA2["email"], "password": USER_DATA2["password"]}
    response: Response = client.post("/login/", data=user_credentials)
    token = Token(**response.json())
    return {"Authorization": f"Bearer {token.access_token}"}


@pytest.fixture
def create_test_post(first_user_authentication_header, client):
    client.post("/posts/", headers=first_user_authentication_header, json=POST1)
    client.post("/posts/", headers=first_user_authentication_header, json=POST2)
    client.post("/posts/", headers=first_user_authentication_header, json=POST3)
