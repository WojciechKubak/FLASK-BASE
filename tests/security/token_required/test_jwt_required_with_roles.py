from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
from flask import Flask


class TestJwtRequiredWithRoles:

    def test_when_unauthorized(self, client: FlaskClient, app: Flask) -> None:
        response = client.get('/protected_route')

        assert 401 == response.status_code
        assert b'Token is missing or invalid' in response.data

    def test_when_insufficient_permissions(self, client: FlaskClient, app: Flask) -> None:
        with app.app_context():
            client = app.test_client()
            access_token = create_access_token(identity='User', additional_claims={'role': 'User'})
            client.set_cookie('access_token_cookie', access_token)

        response = client.get('/protected_route')

        assert 403 == response.status_code
        assert b'Insufficient permissions' in response.data

    def test_when_authenticated(self, client: FlaskClient, app: Flask) -> None:
        with app.app_context():
            client = app.test_client()
            access_token = create_access_token(identity='User', additional_claims={'role': 'Admin'})
            client.set_cookie('access_token_cookie', access_token)

        response = client.get('/protected_route')

        assert 200 == response.status_code
        assert b'Route response' in response.data
