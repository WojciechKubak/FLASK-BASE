from app.routes.user import UserResource, UserActivationResource, UserAdminRoleResource
from app.routes.company import CompanyResource, CompanyListResource
from app.routes.employee import EmployeeResource, EmployeeListResource
from app.routes.statistics import statistics_blueprint
from app.email.configuration import MailConfig
from app.security.configure_security import configure_security
from app.db.configuration import sa
from app.web.configuration import flask_app
from app.config import BaseConfig, DevelopmentConfig, ProductionConfig

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
    """
    Create and configure a Flask application instance.

    Returns:
        Flask: The configured Flask application.
    """
    logging.basicConfig(level=logging.INFO)

    # configuration
    load_dotenv()
    templates_env = Environment(loader=PackageLoader('app', 'templates'))
    setup_config(flask_app)

    with flask_app.app_context():

        sa.init_app(flask_app)

        setup_security(flask_app)
        JWTManager(flask_app)
        configure_security(flask_app)

        setup_mail(flask_app)
        MailConfig.prepare_mail(flask_app, templates_env)

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
    """
    Set up the application configuration based on the selected environment.

    Args:
        app (Flask): The Flask application instance.
    """
    match os.environ.get('APP_CONFIG'):
        case 'development':
            config = DevelopmentConfig
        case 'production':
            config = ProductionConfig
        case _:
            config = BaseConfig
    app.config.from_object(config)


def setup_security(app: Flask) -> None:
    """
    Set up security-related configuration for the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """
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
    """
    Set up email-related configuration for the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """
    mail_settings = {
        'MAIL_SERVER': os.environ.get('MAIL_SERVER'),
        'MAIL_PORT': int(os.environ.get('MAIL_PORT')),
        'MAIL_USE_SSL': ast.literal_eval(os.environ.get('MAIL_USE_SSL')),
        'MAIL_USE_TLS': ast.literal_eval(os.environ.get('MAIL_USE_TLS')),
        'MAIL_USERNAME': os.environ.get('MAIL_USERNAME'),
        'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD')
    }
    app.config.update(mail_settings)
