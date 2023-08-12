from app.security.token_generator import AuthorizationTokenGenerator
from app.service.user import UserService
from flask import Flask, Response, request, make_response
import os


def configure_security(app: Flask) -> None:

    @app.route('/login', methods=['POST'])
    def login() -> Response:
        try:
            data = request.get_json()
            user_service = UserService()
            user = user_service.get_user_by_name(data['username'])
            user_service.check_if_user_is_active(user.username)
            user_service.check_user_password(user.username, data['password'])
        except Exception as e:
            return make_response({'message': str(e)}, 400)

        token_config = {
            'JWT_AUTHTYPE': os.environ.get('JWT_AUTHTYPE'),
            'JWT_SECRET': os.environ.get('JWT_SECRET'),
            'JWT_AUTHMAXAGE': int(os.environ.get('JWT_AUTHMAXAGE')),
            'JWT_REFRESHMAXAGE': int(os.environ.get('JWT_REFRESHMAXAGE'))
        }
        access_token, refresh_token = AuthorizationTokenGenerator(user, token_config).generate_tokens()

        response_body = {
            'access': access_token,
            'refresh': refresh_token
        }
        return make_response(response_body, 201)
