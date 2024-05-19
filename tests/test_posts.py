# 3rd Party
import pytest
from requests import Response
from alembic import command

# Project's modules
from app.schemas import ResponsePostPartModel, ResponsePostModelFull
from app.settings import TEST_MODE

from .settings import alembic_cfg
from .data_for_testing import POST1, POST2, POST3, POST_FOR_UPDATE

if not TEST_MODE:
    exit(1)


class TestPosts:
    def setup_method(self):
        command.downgrade(alembic_cfg, "base")
        command.upgrade(alembic_cfg, "head")

    # CREATE

    @pytest.mark.parametrize("post_data", [POST1, POST2, POST3])
    def test_create_post_first_user(self, first_user_authentication_header, client, post_data):
        response: Response = client.post("/posts/", headers=first_user_authentication_header, json=post_data)
        assert response.status_code == 201
        ResponsePostPartModel(**response.json())

    @pytest.mark.parametrize("post_data", [POST1, POST2, POST3])
    def test_create_post_second_user(self, second_user_authentication_header, client, post_data):
        response: Response = client.post("/posts/", headers=second_user_authentication_header, json=post_data)
        assert response.status_code == 201
        ResponsePostPartModel(**response.json())

    # GET

    def test_get_posts(self, client, create_test_post):
        response: Response = client.get("/posts/")
        assert response.status_code == 200
        for post in response.json():
            ResponsePostModelFull(**post)

    def test_get_empty_list_post(self, client):
        response: Response = client.get("/posts/")
        assert response.status_code == 404
        assert response.json()["detail"] == "Empty list of posts"

    @pytest.mark.parametrize("post_id, title", [(1, POST1["title"]), (2, POST2["title"]), (3, POST3["title"])])
    def test_get_post_by_id(self, client, post_id, title, create_test_post):
        response: Response = client.get(f"/posts/{post_id}")
        post_data = response.json()
        print(post_data)
        assert post_data["Post"]["title"] == title

    # DELETE

    @pytest.mark.parametrize("post_id", [1, 2, 3])
    def test_delete_post(self, client, create_test_post, first_user_authentication_header, post_id):
        response: Response = client.delete(f"/posts/{post_id}", headers=first_user_authentication_header)
        assert response.status_code == 204

    def test_delete_not_existing_post(self, first_user_authentication_header, create_test_post, client):
        not_existing_post_id = 10
        response: Response = client.delete(f"/posts/{not_existing_post_id}", headers=first_user_authentication_header)
        assert response.status_code == 404
        assert response.json()["detail"] == f"Post with id: {not_existing_post_id} was not found"

    @pytest.mark.parametrize("post_id", [1, 2, 3])
    def test_delete_post_not_authorized_user(self, create_test_post, client, post_id):
        response: Response = client.delete(f"/posts/{post_id}")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    @pytest.mark.parametrize("post_id", [1, 2, 3])
    def test_delete_someone_post(self, client, create_test_post, second_user_authentication_header, post_id):
        response: Response = client.delete(f"/posts/{post_id}", headers=second_user_authentication_header)
        assert response.status_code == 403
        assert response.json()["detail"] == "You can't delete someone's post"

    # UPDATE

    @pytest.mark.parametrize("post_id", [1, 2, 3])
    def test_update_post(self, create_test_post, post_id, first_user_authentication_header, client):
        response: Response = client.put(f"/posts/{post_id}", headers=first_user_authentication_header,
                                        json=POST_FOR_UPDATE)
        assert response.status_code == 200
        new_post_data = ResponsePostPartModel(**response.json())
        assert new_post_data.title == POST_FOR_UPDATE["title"]
        assert new_post_data.text == POST_FOR_UPDATE["text"]

    def test_update_not_existing_post(self, create_test_post, first_user_authentication_header, client):
        not_existing_post_id = 10
        response: Response = client.put(f"/posts/{not_existing_post_id}", headers=first_user_authentication_header,
                                        json=POST_FOR_UPDATE)
        assert response.status_code == 404
        assert response.json()["detail"] == f"Post with id: {not_existing_post_id} was not found"

    @pytest.mark.parametrize("post_id", [1, 2, 3])
    def test_update_post_not_authorized_user(self, create_test_post, client, post_id):
        response: Response = client.put(f"/posts/{post_id}")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    @pytest.mark.parametrize("post_id", [1, 2, 3])
    def test_update_someone_post(self, client, create_test_post, second_user_authentication_header, post_id):
        response: Response = client.put(f"/posts/{post_id}", headers=second_user_authentication_header,
                                        json=POST_FOR_UPDATE)
        assert response.status_code == 403
        assert response.json()["detail"] == "You can't update someone's post"
