from app.security.token_required import jwt_required_with_roles
from app.email.configuration import MailConfig
from app.service.user import UserService
from flask_restful import Resource, reqparse
from flask import make_response, Response, request
from datetime import datetime


class UserResource(Resource):
    """
    Resource for managing user accounts.

    This class provides endpoints and functionality for user account management, including user registration and login.

    Attributes:
        parser (reqparse.RequestParser): A request parser for handling incoming JSON data.
    """

    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    parser.add_argument('password', type=str)

    @jwt_required_with_roles(['admin'])
    def get(self, username: str) -> Response:
        """
        Retrieve user information by username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            Response: A response containing user information or an error message.
        """
        try:
            user = UserService().get_user_by_name(username)
            return make_response(user.to_dict(), 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    def post(self, username: str) -> Response:
        """
        Create a new user and send an activation email.

        Args:
            username (str): The desired username for the new user.

        Returns:
            Response: A response indicating whether the user was created and
            the activation email was sent or an error message.
        """
        data = UserResource.parser.parse_args()
        try:
            user = UserService().add_user(data | {'username': username})
            MailConfig.send_activation_mail(user.username, user.email)
            return make_response({'message': 'User created, activation email sent'}, 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['admin'])
    def put(self, username: str) -> Response:
        """
        Update user information.

        Args:
            username (str): The username of the user to update.

        Returns:
            Response: A response containing updated user information or an error message.
        """
        data = UserResource.parser.parse_args()
        try:
            user = UserService().update_user(data | {'username': username})
            return make_response(user.to_dict(), 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['admin'])
    def delete(self, username: str) -> Response:
        """
        Delete a user by username.

        Args:
            username (str): The username of the user to delete.

        Returns:
            Response: A response indicating whether the user was deleted or an error message.
        """
        try:
            id_ = UserService().delete_user(username)
            return make_response({'message': f'Deleted user with id: {id_}'})
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)


class UserActivationResource(Resource):
    """
    Resource for user account activation.
    """

    def get(self) -> Response:
        """
        Activate a user account using an activation link.

        Returns:
            Response: A response indicating whether the user account was successfully activated or an error message.
        """
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
    """
    Resource for managing admin roles for users.
    """

    def post(self, username: str) -> Response:
        """
        Add an admin role to a user.

        Args:
            username (str): The username of the user to add the admin role to.

        Returns:
            Response: A response indicating whether the admin role was added or an error message.
        """
        data = UserResource.parser.parse_args()
        try:
            UserService().add_admin(data | {'username': username})
            return make_response({'message': 'Admin account created'}, 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)
