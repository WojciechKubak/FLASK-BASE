from app.security.token_manager import TokenManager
from app.service.user import UserService
from flask import Flask, Response, request, make_response
import os


def configure_security(app: Flask) -> None:

    token_config = {
        'JWT_AUTHTYPE': os.environ.get('JWT_AUTHTYPE'),
        'JWT_SECRET': os.environ.get('JWT_SECRET'),
        'JWT_AUTHMAXAGE': int(os.environ.get('JWT_AUTHMAXAGE')),
        'JWT_REFRESHMAXAGE': int(os.environ.get('JWT_REFRESHMAXAGE'))
    }
    token_manager = TokenManager(token_config)

    @app.route('/login', methods=['POST'])
    def login() -> Response:
        try:
            data = request.get_json()
            user = UserService().check_login_credentials(data['username'], data['password'])
            return token_manager.generate_response_with_access_tokens(user.username, user.role)
        except Exception as e:
            return make_response({'message': str(e)}, 400)

    @app.route('/refresh', methods=['POST'])
    def refresh() -> Response:
        try:
            token = request.cookies.get('refresh')
            return token_manager.generete_response_with_refreshed_tokens(token)
        except Exception as e:
            return make_response({'message': str(e)}, 400)
