from app.routes.user import UserResource, UserActivationResource, UserAdminRoleResource
from app.routes.company import CompanyResource, CompanyListResource
from app.routes.employee import EmployeeResource, EmployeeListResource
from app.routes.statistics import statistics_blueprint
from app.email.configuration import MailConfig
from app.create_app import setup_security, setup_mail
from app.db.configuration import sa
from app.config import TestingConfig

from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask.testing import FlaskClient
from flask import Flask

from jinja2 import PackageLoader, Environment
import pytest


@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)

    templates_env = Environment(loader=PackageLoader('app', 'templates'))

    app.config.from_object(TestingConfig)
    sa.init_app(app)

    setup_security(app)
    JWTManager(app)

    setup_mail(app)
    MailConfig.prepare_mail(app, templates_env)

    api = Api(app)
    api.add_resource(CompanyListResource, '/companies')
    api.add_resource(CompanyResource, '/companies/<string:company_name>')
    api.add_resource(EmployeeListResource, '/employees')
    api.add_resource(EmployeeResource, '/employees/<string:full_name>')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(UserActivationResource, '/users/activate')
    api.add_resource(UserAdminRoleResource, '/admin/<string:username>')
    app.register_blueprint(statistics_blueprint)

    with app.app_context():
        sa.create_all()

    yield app

    with app.app_context():
        sa.drop_all()


@pytest.fixture
def client(app: Flask) -> None:
    with app.app_context():
        client = app.test_client()
        access_token = create_access_token(identity='User', additional_claims={'role': 'Admin'})
        client.set_cookie('access_token_cookie', access_token)
    yield client
