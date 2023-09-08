from app.model.user import UserModel
from app.db.configuration import sa
from flask.testing import FlaskClient
from datetime import datetime
from flask import Flask
from typing import Any
import os


class TestUserActivationResourcePost:
    current_timestamp = datetime.utcnow().timestamp() * 1000
    token_lifespan = int(os.getenv('REGISTER_TOKEN_LIFESPAN'))

    def test_when_activated(self, client: FlaskClient, app: Flask, user_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(UserModel(**user_model_data))
            sa.session.commit()

        request_data = {
            'timestamp': self.current_timestamp + self.token_lifespan,
            'username': user_model_data['username']
        }
        response = client.get('/users/activate', query_string=request_data)

        assert 200 == response.status_code
        assert b'User activated' in response.data

    def test_when_link_exipres(self, client: FlaskClient, app: Flask, user_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(UserModel(**user_model_data))
            sa.session.commit()

        request_data = {'timestamp': self.current_timestamp, 'username': user_model_data['username']}

        response = client.get('/users/activate', query_string=request_data)

        assert 400 == response.status_code
        assert b'Activation link expired' in response.data

    def test_when_user_does_not_exist(self, client: FlaskClient, app: Flask) -> None:
        request_data = {'timestamp': self.current_timestamp + self.token_lifespan, 'username': 'user'}

        response = client.get('/users/activate', query_string=request_data)

        assert 400 == response.status_code
        assert b'User not found' in response.data

    def test_when_already_activate(self, client: FlaskClient, app: Flask, user_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(UserModel(**user_model_data, is_active=True))
            sa.session.commit()

        request_data = {
            'timestamp': self.current_timestamp + self.token_lifespan,
            'username': user_model_data['username']
        }
        response = client.get('/users/activate', query_string=request_data)

        assert 400 == response.status_code
        assert b'User is already active' in response.data
