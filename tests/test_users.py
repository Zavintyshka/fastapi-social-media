# 3rd Party
import pytest
from fastapi.testclient import TestClient
from requests import Response
from alembic import command

# Project's modules
from app.start_server import app
from app.schemas import ResponseUserModel
from app.database import get_db
from app.settings import TEST_MODE
from .database_for_testing import override_get_db
from .settings import alembic_cfg
from .data_for_testing import USER_DATA, USER_DATA2

app.dependency_overrides[get_db] = override_get_db

if not TEST_MODE:
    exit(1)


class TestUsers:
    def setup_method(self, method):
        command.downgrade(alembic_cfg, "base")
        command.upgrade(alembic_cfg, "head")
        self.client = TestClient(app)

    @pytest.mark.parametrize("user_data", [USER_DATA, USER_DATA2])
    def test_create_user(self, user_data: dict):
        response: Response = self.client.post("/users/", json=user_data)
        assert response.status_code == 201
        returned_data = response.json()
        new_user = ResponseUserModel(**returned_data)
        assert new_user.email == user_data["email"]

    @pytest.mark.parametrize("user_data", [USER_DATA, USER_DATA2])
    def test_user_already_exists(self, user_data: dict):
        self.client.post("/users/", json=user_data)
        response: Response = self.client.post("/users/", json=user_data)
        assert response.status_code == 409
        assert response.json().get("detail") == f"User with email: {user_data["email"]} already exists"

    @pytest.mark.parametrize("user_id, user_firstname", [(1, USER_DATA["firstname"]), (2, USER_DATA2["firstname"])])
    def test_get_user_with_id(self, user_id: int, user_firstname: str):
        self.client.post("/users/", json=USER_DATA)
        self.client.post("/users/", json=USER_DATA2)
        response = self.client.get(f'/users/{user_id}')
        assert response.status_code == 200
        assert response.json().get("firstname") == user_firstname

    def test_get_users(self):
        self.client.post("/users/", json=USER_DATA)
        self.client.post("/users/", json=USER_DATA2)
        response: Response = self.client.get("/users/")
        assert response.status_code == 200
        users = response.json()
        assert len(users) == 2
        user1 = ResponseUserModel(**users[0])
        user2 = ResponseUserModel(**users[1])
        assert user1.email == USER_DATA["email"]
        assert user2.email == USER_DATA2["email"]
