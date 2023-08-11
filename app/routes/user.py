from app.service.user import UserService
from flask_restful import Resource, reqparse
from flask import make_response, Response


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help='email field required')
    parser.add_argument('password', type=str, required=True, help='password field required')
    parser.add_argument('password_repeat', type=str, required=True, help='password_repeat field required')

    def get(self, username: str) -> Response:
        try:
            user = UserService().get_user_by_name(username)
            return make_response(user.to_dict(), 200)
        except Exception as e:
            return make_response({'message': e.args[0]}, 400)

    def post(self, username: str) -> Response:
        data = UserResource.parser.parse_args()
        try:
            UserService().add_user(data | {'username': username})
            return make_response({'message': 'User created'}, 201)
        except Exception as e:
            return make_response({'message': e.args[0]}, 400)

    def put(self, username: str) -> Response:
        data = UserResource.parser.parse_args()
        try:
            UserService().update_user(data | {'username': username})
            return make_response({'message': 'User updated'}, 201)
        except Exception as e:
            return make_response({'message': e.args[0]}, 400)

    def delete(self, username: str) -> Response:
        try:
            UserService().delete_user(username)
            return make_response({'message': 'User deleted'})
        except Exception as e:
            return make_response({'message': e.args[0]}, 400)
