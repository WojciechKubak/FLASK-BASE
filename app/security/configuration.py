from app.service.user import UserService
from flask import Flask, Response, request, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, \
    set_access_cookies, set_refresh_cookies, unset_jwt_cookies


def configure_security(app: Flask) -> None:

    @app.route("/login", methods=["POST"])
    def login() -> Response:
        data = request.get_json()
        user = UserService().check_login_credentials(data['username'], data['password'])

        response = make_response({'message': "Login successful"})
        access_token = create_access_token(identity=user.username, additional_claims={'role': user.role})
        refresh_token = create_refresh_token(identity="example_user", additional_claims={'role': user.role})

        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        return response

    @app.route("/logout", methods=["POST"])
    def logout() -> Response:
        response = make_response({'message': "Logout successful"})
        unset_jwt_cookies(response)
        return response
