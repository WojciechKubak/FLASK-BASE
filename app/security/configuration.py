from app.security.token_generator import AuthorizationTokenGenerator
from app.service.user import UserService
from flask import Flask, Response, request, make_response
import jwt
import os


def configure_security(app: Flask) -> None:

    token_config = {
        'JWT_AUTHTYPE': os.environ.get('JWT_AUTHTYPE'),
        'JWT_SECRET': os.environ.get('JWT_SECRET'),
        'JWT_AUTHMAXAGE': int(os.environ.get('JWT_AUTHMAXAGE')),
        'JWT_REFRESHMAXAGE': int(os.environ.get('JWT_REFRESHMAXAGE'))
    }

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

        access_token, refresh_token = AuthorizationTokenGenerator(
            user.username,
            user.role,
            token_config
        ).generate_tokens()

        response_body = {'access': access_token, 'refresh': refresh_token}
        response = make_response(response_body, 201)
        response.set_cookie('access', access_token, httponly=True)
        response.set_cookie('refresh', refresh_token, httponly=True)

        return response

    @app.route('/refresh', methods=['POST'])
    def refresh() -> Response:
        token = request.cookies.get('refresh')
        decoded_token_data = jwt.decode(
            token,
            token_config['JWT_SECRET'],
            algorithms=[token_config['JWT_AUTHTYPE']]
        )

        access_token, refresh_token = AuthorizationTokenGenerator(
            decoded_token_data['sub'],
            decoded_token_data['role'],
            token_config
        ).generate_tokens()

        response_body = {'access': access_token, 'refresh': refresh_token}
        response = make_response(response_body, 201)
        response.set_cookie('access', access_token, httponly=True)
        response.set_cookie('refresh', refresh_token, httponly=True)

        return response





# def token_required(roles: list[str]):
#     def decorator(func):
#         @wraps(func)
#         def decorated(*args, **kwargs):
#             header = request.headers.get('Authorization')
#
#             if not header:
#                 return make_response({'message': 'No token provided'}, 401)
#
#             if not header.startswith(os.environ.get('JWT_PREFIX')):
#                 return make_response({'message': 'Invalid token provided'}, 401)
#
#             token = header.split(' ')[1]
#
#             try:
#                 data = jwt.decode(token, os.environ.get('JWT_SECRET'), algorithms=[os.environ.get('JWT_AUTHTYPE')])
#                 if data['role'].lower() not in [role.lower() for role in roles]:
#                     return make_response({'message': 'Acces denied'}, 403)
#             except:
#                 return make_response({'message': 'Authentication error'}, 401)
#
#             return func(*args, **kwargs)
#
#         return decorated
#     return decorator
