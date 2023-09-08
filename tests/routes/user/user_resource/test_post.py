from app.model.user import UserModel
from app.db.configuration import sa
from flask.testing import FlaskClient
from flask import Flask
from typing import Any


class TestUserResourcePost:

    def test_when_added(self, client: FlaskClient, app: Flask, user_model_data: dict[str, Any]) -> None:
        response = client.post(f"users/{user_model_data.pop('username')}", json=user_model_data)

        assert 201 == response.status_code
        assert b'activation email sent' in response.data

    def test_when_user_exists(self, client: FlaskClient, app: Flask, user_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(UserModel(**user_model_data))
            sa.session.commit()

        response = client.post(f"users/{user_model_data.pop('username')}", json=user_model_data)

        assert 400 == response.status_code
        assert b'User already exists' in response.data

    def test_when_validation_error_occurs(self, client: FlaskClient, app: Flask) -> None:
        response = client.post('users/Username', json={})

        assert 400 == response.status_code
        assert b'field required' in response.data
