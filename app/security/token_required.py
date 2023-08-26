from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import make_response
from functools import wraps
from typing import Callable, Any


def token_required(roles: list[str]) -> Callable:
    def decorator(func: Callable) -> Callable:

        @wraps(func)
        def decorated(*args: tuple[Any], **kwargs: dict[str, Any]) -> Callable:
            try:
                verify_jwt_in_request()
                role = get_jwt()['role']
            except Exception:
                return make_response({'message': 'Authentication error'}, 401)

            if role.lower() in [role.lower() for role in roles]:
                return func(*args, **kwargs)

            return make_response({'message': 'Unauthorized'}, 403)

        return decorated
    return decorator
