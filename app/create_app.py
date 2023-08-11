from app.db.configuration import sa
from app.db.connection import MySQLConnectionPoolBuilder
from app.routes.company import CompanyResource, CompanyListResource
from app.routes.employee import EmployeeResource, EmployeeListResource
from app.routes.statistics.routes import statistics_blueprint
from flask import jsonify, Flask
from flask_restful import Api
import logging

app = Flask(__name__)


def create_app():
    logging.basicConfig(level=logging.INFO)

    with app.app_context():

        # database configuration
        url = MySQLConnectionPoolBuilder().set_host('mysql').build_connection_string()
        app.config['SQLALCHEMY_DATABASE_URI'] = url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        sa.init_app(app)

        # register blueprints
        app.register_blueprint(statistics_blueprint)

        @app.route('/')
        def index():
            return jsonify({'message': 'This is home page'})

        # register resources
        api = Api(app)
        api.add_resource(CompanyListResource, '/companies')
        api.add_resource(CompanyResource, '/companies/<string:company_name>')
        api.add_resource(EmployeeListResource, '/employees')
        api.add_resource(EmployeeResource, '/employees/<string:full_name>')

        return app
