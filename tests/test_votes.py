# 3rd Party
import pytest
from requests import Response
from alembic import command

# Project's modules
from app.schemas import ResponsePostPartModel
from app.settings import TEST_MODE

from .settings import alembic_cfg

if not TEST_MODE:
    exit(1)


class TestVotes:
    def setup_method(self):
        command.downgrade(alembic_cfg, "base")
        command.upgrade(alembic_cfg, "head")

    @pytest.mark.parametrize("post_id", [1, 2, 3])
    def test_set_one_like_to_post(self, second_user_authentication_header, create_test_post, client, post_id):
        vote_form = {"post_id": post_id, "vote_status": "like"}
        response: Response = client.post("/vote/", json=vote_form, headers=second_user_authentication_header)
        assert response.status_code == 201
        ResponsePostPartModel(**response.json())
        post = client.get(f"/posts/{post_id}").json()
        assert post["Post"]["id"] == post_id
        assert post["likes"] == 1

    @pytest.mark.parametrize("post_id", [1, 2, 3])
    def test_set_many_likes_to_post(self, first_user_authentication_header, second_user_authentication_header,
                                    create_test_post, client, post_id):
        vote_form = {"post_id": post_id, "vote_status": "like"}
        response1: Response = client.post("/vote/", json=vote_form, headers=first_user_authentication_header)
        response2: Response = client.post("/vote/", json=vote_form, headers=second_user_authentication_header)
        assert response1.status_code == 201
        assert response2.status_code == 201
        post = client.get(f"/posts/{post_id}").json()
        assert post["Post"]["id"] == post_id
        assert post["likes"] == 2

    @pytest.mark.parametrize("post_id", [1, 2, 3])
    def test_unlike_post(self, second_user_authentication_header, create_test_post, client, post_id):
        like_form = {"post_id": post_id, "vote_status": "like"}
        unlike_form = {"post_id": post_id, "vote_status": "unlike"}
        response: Response = client.post("/vote/", json=like_form, headers=second_user_authentication_header)
        assert response.status_code == 201
        post = client.get(f"/posts/{post_id}").json()
        assert post["Post"]["id"] == post_id
        assert post["likes"] == 1
        response: Response = client.post("/vote/", json=unlike_form, headers=second_user_authentication_header)
        assert response.status_code == 201
        post = client.get(f"/posts/{post_id}").json()
        assert post["Post"]["id"] == post_id
        assert post["likes"] == 0

    @pytest.mark.parametrize("post_id", [1, 2, 3])
    def test_not_authorized_user(self, create_test_post, client, post_id):
        vote_form = {"post_id": post_id, "vote_status": "like"}
        response: Response = client.post("/vote/", json=vote_form)
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    @pytest.mark.parametrize("post_id", [1, 2, 3])
    def test_set_double_like_to_post(self, second_user_authentication_header, create_test_post, client, post_id):
        vote_form = {"post_id": post_id, "vote_status": "like"}
        client.post("/vote/", json=vote_form, headers=second_user_authentication_header)
        response: Response = client.post("/vote/", json=vote_form, headers=second_user_authentication_header)
        assert response.status_code == 409

    @pytest.mark.parametrize("post_id", [1, 2, 3])
    def test_unlike_to_post_exception(self, second_user_authentication_header, create_test_post, client, post_id):
        vote_form = {"post_id": post_id, "vote_status": "unlike"}
        response: Response = client.post("/vote/", json=vote_form, headers=second_user_authentication_header)
        assert response.status_code == 409

    def test_like_to_not_existing_post(self, client, second_user_authentication_header):
        not_existing_post_like_from = {"post_id": 100, "vote_status": "like"}
        response: Response = client.post("/vote/", json=not_existing_post_like_from,
                                         headers=second_user_authentication_header)
        assert response.status_code == 404
        assert response.json()["detail"] == f"Post with id: {not_existing_post_like_from["post_id"]} was not found"
