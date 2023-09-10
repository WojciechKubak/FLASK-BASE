from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from flask import make_response
from functools import wraps
from typing import Callable, Any


def jwt_required_with_roles(roles: list[str]) -> Callable:
    """
    Decorator for requiring JWT authentication with specific roles.

    Args:
        roles (list[str]): A list of role names that are allowed to access the protected endpoint.

    Returns:
        Callable: A decorator function that can be used to protect Flask routes.
    """
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def decorated(*args: tuple[Any], **kwargs: dict[str, Any]):
            try:
                verify_jwt_in_request()
                if get_jwt().get('role').lower() in [role.lower() for role in roles]:
                    return fn(*args, **kwargs)
                else:
                    return make_response({'message': 'Insufficient permissions'}, 403)
            except (NoAuthorizationError, InvalidHeaderError):
                return make_response({'message': 'Token is missing or invalid'}, 401)

        return decorated
    return decorator
