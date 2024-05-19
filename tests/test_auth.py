# 3rd Party
import pytest
from fastapi.testclient import TestClient
from requests import Response
from alembic import command
from jose import jwt

# Project's modules
from app.start_server import app
from app.database import get_db
from app.schemas import Token
from app.settings import TEST_MODE
from app.settings import settings
from .database_for_testing import override_get_db
from .settings import alembic_cfg
from .data_for_testing import USER_DATA, USER_DATA2

app.dependency_overrides[get_db] = override_get_db

if not TEST_MODE:
    exit(1)


class TestAuth:

    def setup_method(self, method):
        command.downgrade(alembic_cfg, "base")
        command.upgrade(alembic_cfg, "head")
        self.client = TestClient(app)

    @pytest.mark.parametrize("user_data", [USER_DATA, USER_DATA2])
    def test_login(self, user_data: dict):
        created_user = self.client.post("/users/", json=user_data).json()
        user_id = created_user["id"]

        user_credentials = {"username": user_data["email"], "password": user_data["password"]}
        response: Response = self.client.post("/login/", data=user_credentials)
        returned_data = response.json()
        assert response.status_code == 200
        returned_token = Token(**returned_data)
        decoded_jwt = jwt.decode(returned_token.access_token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        assert user_id == decoded_jwt["user_id"]
        assert returned_token.token_type == "bearer"

    @pytest.mark.parametrize("user_data", [USER_DATA, USER_DATA2])
    def test_login_wrong_password(self, user_data: dict):
        self.client.post("/users/", json=user_data).json()

        wrong_password = "32ru2fev3g"
        user_credentials = {"username": user_data["email"], "password": wrong_password}
        response: Response = self.client.post("/login/", data=user_credentials)
        returned_data = response.json()
        assert response.status_code == 403
        assert returned_data["detail"] == "Wrong password"

    @pytest.mark.parametrize("user_data", [USER_DATA, USER_DATA2])
    def test_login_failure_wrong_email(self, user_data: dict):
        self.client.post("/users/", json=user_data).json()

        wrong_email = "32ru2fev3g"
        user_credentials = {"username": wrong_email, "password": user_data["password"]}
        response: Response = self.client.post("/login/", data=user_credentials)
        returned_data = response.json()
        assert response.status_code == 403
        assert returned_data["detail"] == f"User with email {wrong_email} not found"
