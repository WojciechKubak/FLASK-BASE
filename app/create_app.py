from app.web.configuration import app
from app.db.configuration import sa
from app.db.connection import MySQLConnectionPoolBuilder
from flask import jsonify
import logging


def create_app():
    logging.basicConfig(level=logging.INFO)

    with app.app_context():

        # database configuration
        url = MySQLConnectionPoolBuilder().set_config_params({'host': 'mysql'}).build_connection_string()
        app.config['SQLALCHEMY_DATABASE_URI'] = url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        sa.init_app(app)

        @app.route('/')
        def index():
            return jsonify({'message': 'This is home page'})

        return app
