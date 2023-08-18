from app.security.token_manager import TokenManager
from flask import request, make_response
from functools import wraps
from typing import Callable, Any


def token_required(roles: list[str]) -> Callable:
    def decorator(func: Callable) -> Callable:

        @wraps(func)
        def decorated(*args: tuple[Any], **kwargs: dict[str, Any]) -> Callable:
            if not (token := request.cookies.get('access')):
                return make_response({'message': 'No token provided'}, 401)
            try:
                token_data = TokenManager().decode_token(token)
                if token_data['role'].lower() not in [role.lower() for role in roles]:
                    return make_response({'message': 'Acces denied'}, 403)
            except Exception:
                return make_response({'message': 'Authentication error'}, 401)

            return func(*args, **kwargs)

        return decorated
    return decorator
