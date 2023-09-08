from flask.testing import FlaskClient
from flask import Flask
from typing import Any


def test_when_authenticated(client: FlaskClient, app: Flask, user_model_data: dict[str, Any]) -> None:
    credentials = {
        'username': user_model_data['username'],
        'password': user_model_data['password']
    }
    client.post('/login', json=credentials)

    response_logout = client.post('/logout')

    assert response_logout.status_code == 200
    assert b'Logout successful' in response_logout.data
    assert not client.get_cookie('access_token_cookie')
