from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from flask import make_response
from functools import wraps
from typing import Callable, Any


def jwt_required_with_roles(roles: list[str]) -> Callable:
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def decorated(*args: tuple[Any], **kwargs: dict[str, Any]):
            try:
                verify_jwt_in_request()
                role = get_jwt_identity()
                if role.lower() in [role.lower() for role in roles]:
                    return fn(*args, **kwargs)
                else:
                    return make_response({'message': 'Insufficient permissions'}, 403)
            except (NoAuthorizationError, InvalidHeaderError):
                return make_response({'message': 'Token is missing or invalid'}, 401)

        return decorated
    return decorator
