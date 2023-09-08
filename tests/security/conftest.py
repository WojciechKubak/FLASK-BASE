from app.config import TestingConfig
from app.create_app import setup_security
from app.db.configuration import sa
from app.security.token_required import jwt_required_with_roles
from app.security.configure_security import configure_security

from flask_jwt_extended import JWTManager
from flask import Flask, Response, make_response

import pytest


@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)

    app.config.from_object(TestingConfig)
    sa.init_app(app)

    setup_security(app)
    configure_security(app)
    JWTManager(app)

    with app.app_context():
        sa.create_all()

        @app.route('/protected_route', methods=['GET'])
        @jwt_required_with_roles(['Admin'])
        def foo() -> Response:
            return make_response({'message': 'Route response'}, 200)

    yield app

    with app.app_context():
        sa.drop_all()


@pytest.fixture
def client(app: Flask) -> None:
    with app.app_context():
        client = app.test_client()
    yield client
