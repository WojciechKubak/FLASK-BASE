from app.routes.user import UserResource, UserActivationResource, UserAdminRoleResource
from app.routes.company import CompanyResource, CompanyListResource
from app.routes.employee import EmployeeResource, EmployeeListResource
from app.routes.statistics import statistics_blueprint
from app.email.configuration import MailConfig
from app.security.configure_security import configure_security
from app.db.configuration import sa
from app.web.configuration import flask_app
from app.db.connection import ConnectionPoolBuilder

from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask import Response, make_response
from flask import Flask

from jinja2 import PackageLoader, Environment
from dotenv import load_dotenv
import logging
import ast
import os


def create_app() -> Flask:
    logging.basicConfig(level=logging.INFO)

    # configuration
    load_dotenv()
    templates_env = Environment(loader=PackageLoader('app', 'templates'))
    setup_config(flask_app)

    with flask_app.app_context():

        # security
        setup_security(flask_app)
        JWTManager(flask_app)
        configure_security(flask_app)

        # mail
        setup_mail(flask_app)
        MailConfig.prepare_mail(flask_app, templates_env)

        # routes
        api = Api(flask_app)
        api.add_resource(CompanyListResource, '/companies')
        api.add_resource(CompanyResource, '/companies/<string:company_name>')
        api.add_resource(EmployeeListResource, '/employees')
        api.add_resource(EmployeeResource, '/employees/<string:full_name>')
        api.add_resource(UserResource, '/users/<string:username>')
        api.add_resource(UserActivationResource, '/users/activate')
        api.add_resource(UserAdminRoleResource, '/admin/<string:username>')
        flask_app.register_blueprint(statistics_blueprint)

        @flask_app.route('/')
        def index() -> Response:
            return make_response({'message': 'Home page'}, 200)

        return flask_app


def setup_config(app: Flask) -> None:
    url = ConnectionPoolBuilder.builder().set_host('mysql').build_connection_string()
    config = {
        'SQLALCHEMY_DATABASE_URI': url,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }
    app.config.update(config)
    sa.init_app(app)


def setup_security(app: Flask) -> None:
    jwt_settings = {
        'JWT_COOKIE_SECURE': ast.literal_eval(os.environ.get('JWT_COOKIE_SECURE')),
        'JWT_TOKEN_LOCATION': ast.literal_eval(os.environ.get('JWT_TOKEN_LOCATION')),
        'JWT_SECRET_KEY': os.environ.get('JWT_SECRET_KEY'),
        'JWT_ACCESS_TOKEN_EXPIRES': int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES')),
        'JWT_REFRESH_TOKEN_EXPIRES': int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES')),
        'JWT_COOKIE_CSRF_PROTECT': ast.literal_eval(os.environ.get('JWT_COOKIE_CSRF_PROTECT'))
    }
    app.config.update(jwt_settings)


def setup_mail(app: Flask) -> None:
    mail_settings = {
        'MAIL_SERVER': os.environ.get('MAIL_SERVER'),
        'MAIL_PORT': int(os.environ.get('MAIL_PORT')),
        'MAIL_USE_SSL': ast.literal_eval(os.environ.get('MAIL_USE_SSL')),
        'MAIL_USE_TLS': ast.literal_eval(os.environ.get('MAIL_USE_TLS')),
        'MAIL_USERNAME': os.environ.get('MAIL_USERNAME'),
        'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD')
    }
    app.config.update(mail_settings)
