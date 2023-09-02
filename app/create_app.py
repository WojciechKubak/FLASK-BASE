from app.web.configuration import flask_app
from app.config import BaseConfig, ProductionConfig, DevelopmentConfig
from app.routes.company import CompanyResource, CompanyListResource
from app.routes.employee import EmployeeResource, EmployeeListResource
from app.routes.statistics import statistics_blueprint
from app.email.configuration import MailConfig
from app.routes.user import UserResource, UserActivationResource, UserAdminRoleResource
from app.security.configuration import configure_security
from app.db.configuration import sa
from flask_jwt_extended import JWTManager
from flask_restful import Api
from jinja2 import PackageLoader, Environment
from dotenv import load_dotenv
from alembic.config import Config, command
from flask import Response, make_response
import app.signals
import logging
import ast
import os


def create_app():

    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    match os.environ.get('APP_ENV'):
        case 'production':
            app_config = ProductionConfig()
        case 'development':
            app_config = DevelopmentConfig()
        case _:
            app_config = BaseConfig()

    alembic_cfg = Config('alembic.ini')
    alembic_cfg.set_main_option('sqlalchemy.url', app_config.SQLALCHEMY_DATABASE_URI)
    command.upgrade(alembic_cfg, 'head')

    templates_env = Environment(loader=PackageLoader('app', 'templates'))

    with flask_app.app_context():

        flask_app.config.from_object(app_config)
        sa.init_app(flask_app)

        jwt_settings = {
            'JWT_COOKIE_SECURE': ast.literal_eval(os.environ.get('JWT_COOKIE_SECURE')),
            'JWT_TOKEN_LOCATION': ast.literal_eval(os.environ.get('JWT_TOKEN_LOCATION')),
            'JWT_SECRET_KEY': os.environ.get('JWT_SECRET_KEY'),
            'JWT_ACCESS_TOKEN_EXPIRES': int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES')),
            'JWT_REFRESH_TOKEN_EXPIRES': int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES')),
            'JWT_COOKIE_CSRF_PROTECT': ast.literal_eval(os.environ.get('JWT_COOKIE_CSRF_PROTECT'))
        }
        flask_app.config.update(jwt_settings)
        jwt = JWTManager(flask_app)

        mail_settings = {
            'MAIL_SERVER': os.environ.get('MAIL_SERVER'),
            'MAIL_PORT': int(os.environ.get('MAIL_PORT')),
            'MAIL_USE_SSL': ast.literal_eval(os.environ.get('MAIL_USE_SSL')),
            'MAIL_USE_TLS': ast.literal_eval(os.environ.get('MAIL_USE_TLS')),
            'MAIL_USERNAME': os.environ.get('MAIL_USERNAME'),
            'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD')
        }
        flask_app.config.update(mail_settings)
        MailConfig.prepare_mail(flask_app, templates_env)

        configure_security(flask_app)

        flask_app.register_blueprint(statistics_blueprint)

        @flask_app.route('/')
        def index() -> Response:
            return make_response({'message': 'Home page'}, 200)

        api = Api(flask_app)

        api.add_resource(CompanyListResource, '/companies')
        api.add_resource(CompanyResource, '/companies/<string:company_name>')
        api.add_resource(EmployeeListResource, '/employees')
        api.add_resource(EmployeeResource, '/employees/<string:full_name>')
        api.add_resource(UserResource, '/users/<string:username>')
        api.add_resource(UserActivationResource, '/users/activate')
        api.add_resource(UserAdminRoleResource, '/admin/<string:username>')

        return flask_app
