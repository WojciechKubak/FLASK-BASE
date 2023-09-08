from app.email.configuration import MailConfig
from app.config import TestingConfig
from flask.testing import FlaskClient
from jinja2 import PackageLoader, Environment
from flask import Flask
import pytest
import ast
import os


@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)

    app.config.from_object(TestingConfig)

    templates_env = Environment(loader=PackageLoader('app', 'templates'))

    mail_settings = {
        'MAIL_SERVER': os.environ.get('MAIL_SERVER'),
        'MAIL_PORT': int(os.environ.get('MAIL_PORT')),
        'MAIL_USE_SSL': ast.literal_eval(os.environ.get('MAIL_USE_SSL')),
        'MAIL_USE_TLS': ast.literal_eval(os.environ.get('MAIL_USE_TLS')),
        'MAIL_USERNAME': os.environ.get('MAIL_USERNAME'),
        'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD')
    }
    app.config.update(mail_settings)
    MailConfig.prepare_mail(app, templates_env)

    yield app


@pytest.fixture
def mail_client(app: Flask) -> FlaskClient:
    return app.test_client()
