from app.web.configuration import flask_app
from flask import make_response, Response


@flask_app.errorhandler(404)
def not_found_error(error: int) -> Response:
    return make_response({'message': 'The requested resource was not found.'}, error)


@flask_app.errorhandler(500)
def internal_server_error(error: int):
    return make_response({'message': 'Internal server error'}, error)
