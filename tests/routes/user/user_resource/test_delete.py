from app.model.user import UserModel
from app.db.configuration import sa
from flask.testing import FlaskClient
from flask import Flask
from typing import Any


class TestUserResourceDelete:

    def test_when_deleted(self, client: FlaskClient, app: Flask, user_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(UserModel(**user_model_data))
            sa.session.commit()

        response = client.delete(f"/users/{user_model_data['username']}")

        assert 200 == response.status_code
        assert b'Deleted user with id' in response.data

    def test_when_user_does_not_exist(self, client: FlaskClient) -> None:
        response = client.delete('/users/User')

        assert 400 == response.status_code
        assert b'User not found' in response.data
