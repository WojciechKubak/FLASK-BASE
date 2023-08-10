from app.model.user import UserModel
from flask_restful import Resource, reqparse
from flask import make_response, Response


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='username field required')
    parser.add_argument('email', type=str, required=True, help='email field required')
    parser.add_argument('password', type=str, required=True, help='password field required')
    parser.add_argument('password_repeat', type=str, required=True, help='password_repeat field required')

    def get(self) -> Response:
        pass

    def post(self) -> Response:
        request_data = UserResource.parser.parse_args()
        # logging.info(request_data)
        if UserModel.find_by_username(request_data['username']):
            return make_response({'message': 'User already exists.'}, 400)
        if UserModel.find_by_email(request_data['email']):
            return make_response({'message': 'Email already exists.'}, 400)
        if request_data['password'] != request_data['password_repeat']:
            return make_response({'message': 'Passwords must be the same.'}, 400)

        user = UserModel(**request_data)
        user.add_or_update()

        return make_response({'message': 'User created successfully.'}, 201)

    def delete(self) -> Response:
        ...

    def put(self) -> Response:
        pass
