from app.model.user import UserModel
from app.db.configuration import sa
from flask.testing import FlaskClient
from flask import Flask
from typing import Any


class TestUserResourcePut:

    def test_when_updated(self, client: FlaskClient, app: Flask, user_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(UserModel(**user_model_data))
            sa.session.commit()

        changes = {'email': 'new@example.com'}
        response = client.put(f"users/{user_model_data.pop('username')}", json=user_model_data | changes)

        assert 201 == response.status_code
        assert changes['email'] == response.json['email']

    def test_when_validation_error_occurs(self, client: FlaskClient, app: Flask) -> None:
        with app.app_context():
            sa.session.add(UserModel(username='user', password=''))
            sa.session.commit()

        response = client.put('users/user', json={})

        assert 400 == response.status_code
        assert b'field required' in response.data

    def test_when_user_not_found(self, client: FlaskClient, app: Flask) -> None:
        response = client.put('users/user', json={})

        assert 400 == response.status_code
        assert b'User not found' in response.data
