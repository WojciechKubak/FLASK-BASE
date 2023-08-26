from app.web.configuration import flask_app
from app.db.connection import MySQLConnectionPoolBuilder
from app.routes.company import CompanyResource, CompanyListResource
from app.routes.employee import EmployeeResource, EmployeeListResource
from app.routes.statistics import statistics_blueprint
from app.email.configuration import MailConfig
from app.routes.user import UserResource, UserActivationResource, UserAdminRoleResource
from app.security.configuration import configure_security
from app.db.configuration import sa
from flask_jwt_extended import JWTManager
from flask import jsonify
from flask_restful import Api
from jinja2 import PackageLoader, Environment
from dotenv import load_dotenv
import app.signals
import logging
import ast
import os


def create_app():

    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    templates_env = Environment(loader=PackageLoader('app', 'templates'))

    with flask_app.app_context():

        # database configuration
        url = MySQLConnectionPoolBuilder().set_host('mysql').build_connection_string()
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = url
        flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        sa.init_app(flask_app)

        # security configuration
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

        # email configuration
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

        # configure security
        configure_security(flask_app)

        # register blueprints
        flask_app.register_blueprint(statistics_blueprint)

        @flask_app.route('/')
        def index():
            return jsonify({'message': 'This is home page'})

        api = Api(flask_app)

        # register resources
        api.add_resource(CompanyListResource, '/companies')
        api.add_resource(CompanyResource, '/companies/<string:company_name>')
        api.add_resource(EmployeeListResource, '/employees')
        api.add_resource(EmployeeResource, '/employees/<string:full_name>')
        api.add_resource(UserResource, '/users/<string:username>')
        api.add_resource(UserActivationResource, '/users/activate')
        api.add_resource(UserAdminRoleResource, '/admin/<string:username>')

        return flask_app
