from app.model.user import UserModel
from app.db.configuration import sa
from flask.testing import FlaskClient
from flask import Flask
from typing import Any


class TestConfigureSecurityLogin:

    def test_when_user_does_not_exist(self, client: FlaskClient) -> None:
        response = client.post('/login', json={'username': 'User', 'password': 'password'})

        assert 401 == response.status_code
        assert b'User not found' in response.data

    def test_when_password_is_incorrect(self, app: Flask, client: FlaskClient, user_model_data: dict[str, Any]) -> None:
        credentials = {
            'username': user_model_data['username'],
            'password': f"{user_model_data['password']}11"
        }
        response = client.post('/login', json=credentials)

        assert 401 == response.status_code
        assert b'Incorrect password provided' in response.data

    def test_when_user_is_not_active(self, app: Flask, client: FlaskClient, user_model_data: dict[str, Any]) -> None:
        with app.app_context():
            user = sa.session.query(UserModel).filter_by(username=user_model_data['username']).first()
            user.is_active = False
            sa.session.commit()

        credentials = {
            'username': user_model_data['username'],
            'password': user_model_data['password']
        }
        response = client.post('/login', json=credentials)

        assert 401 == response.status_code
        assert b'User is not activated' in response.data

    def test_when_logged_in_succesfully(self, app: Flask, client: FlaskClient, user_model_data: dict[str, Any]) -> None:
        credentials = {
            'username': user_model_data['username'],
            'password': user_model_data['password']
        }
        response = client.post('/login', json=credentials)

        assert 200 == response.status_code
        assert b'Login successful' in response.data
        assert 'access_token_cookie' in response.headers['Set-Cookie']
