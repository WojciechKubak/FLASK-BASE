from flask import jsonify
from app.web.configuration import app
import logging


def create_app():
    logging.basicConfig(level=logging.INFO)
    with app.app_context():

        @app.route('/')
        def index():
            return jsonify({'message': 'This is home page.'})

        return app
