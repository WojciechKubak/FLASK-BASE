from app.model.user import UserModel
from app.db.configuration import sa
from flask.testing import FlaskClient
from flask import Flask
from typing import Any


class TestUserResourceGet:

    def test_when_user_exists(self, client: FlaskClient, app: Flask, user_model_data: dict[str, Any]) -> None:
        with app.app_context():
            user = UserModel(**user_model_data)
            sa.session.add(user)

            response = client.get(f"users/{user_model_data['username']}")

            assert 200 == response.status_code
            assert user.to_dict() == response.json

    def test_when_user_does_not_exists(self, client: FlaskClient, app: Flask) -> None:
        response = client.get('/users/User')

        assert 400 == response.status_code
        assert b'User not found' in response.data
