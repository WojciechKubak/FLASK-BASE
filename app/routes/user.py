from app.security.token_required import jwt_required_with_roles
from app.email.configuration import MailConfig
from app.service.user import UserService
from flask_restful import Resource, reqparse
from flask import make_response, Response, request
from datetime import datetime


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    parser.add_argument('password', type=str)

    @jwt_required_with_roles(['admin'])
    def get(self, username: str) -> Response:
        try:
            user = UserService().get_user_by_name(username)
            return make_response(user.to_dict(), 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    def post(self, username: str) -> Response:
        data = UserResource.parser.parse_args()
        try:
            user = UserService().add_user(data | {'username': username})
            MailConfig.send_activation_mail(user.username, user.email)
            return make_response({'message': 'User created, activation email sent'}, 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['admin'])
    def put(self, username: str) -> Response:
        data = UserResource.parser.parse_args()
        try:
            user = UserService().update_user(data | {'username': username})
            return make_response(user.to_dict(), 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['admin'])
    def delete(self, username: str) -> Response:
        try:
            id_ = UserService().delete_user(username)
            return make_response({'message': f'Deleted user with id: {id_}'})
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)


class UserActivationResource(Resource):

    def get(self) -> Response:
        timestamp = float(request.args.get('timestamp'))
        if timestamp < datetime.utcnow().timestamp() * 1000:
            return make_response({'message': 'Activation link expired'}, 400)
        try:
            user_service = UserService()
            user = user_service.get_user_by_name(request.args.get('username'))
            user_service.activate_user(user.username)
            return make_response({'message': 'User activated'}, 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)


class UserAdminRoleResource(Resource):

    def post(self, username: str) -> Response:
        data = UserResource.parser.parse_args()
        try:
            UserService().add_user(data | {'username': username}, is_admin=True)
            return make_response({'message': 'Admin account created'}, 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)
