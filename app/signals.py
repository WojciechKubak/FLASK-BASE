from app.web.configuration import flask_app
from flask_jwt_extended import create_access_token, set_access_cookies, get_jwt_identity, get_jwt
from flask import Response, request
from datetime import datetime, timezone, timedelta
import logging
import os


logging.basicConfig(level=logging.INFO)


@flask_app.before_request
def log_request_started() -> None:
    """
    Log the start of each request.

    Logs request details including the client's IP address, URL, HTTP method, and headers.
    """
    logging.info('Request started')
    logging.info(f'{request.remote_addr=}')
    logging.info(f'{request.url=}')
    logging.info(f"{request.method=}")
    logging.info(f"{request.headers=}")


@flask_app.after_request
def refresh_expiring_jwts(response: Response) -> Response:
    """
    Refresh expiring JWT access tokens.

    This middleware checks if the JWT access token is about to expire and refreshes it if necessary.

    Args:
        response (Response): The Flask response object.

    Returns:
        Response: The updated Flask response object.
    """
    try:
        refresh_token_data = get_jwt()
        refresh_exp, role = refresh_token_data['exp'], refresh_token_data['role']

        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(seconds=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES'))))
        if target_timestamp > refresh_exp:
            access_token = create_access_token(identity=get_jwt_identity(), additional_claims={'role': role})
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response
