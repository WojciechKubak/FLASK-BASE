from flask import request, make_response
from functools import wraps
from typing import Callable, Any
import jwt
import os


def token_required(roles: list[str]) -> Callable:

    def decorator(func: Callable) -> Callable:

        @wraps(func)
        def decorated(*args: tuple[Any], **kwargs: dict[str, Any]) -> Callable:
            header = request.headers.get('Authorization')

            if not header:
                return make_response({'message': 'No token provided'}, 401)

            if not header.startswith(os.environ.get('JWT_PREFIX')):
                return make_response({'message': 'Invalid token provided'}, 401)

            token = header.split(' ')[1]

            try:
                data = jwt.decode(token, os.environ.get('JWT_SECRET'), algorithms=[os.environ.get('JWT_AUTHTYPE')])
                if data['role'].lower() not in [role.lower() for role in roles]:
                    return make_response({'message': 'Acces denied'}, 403)
            except Exception:
                return make_response({'message': 'Authentication error'}, 401)

            return func(*args, **kwargs)

        return decorated

    return decorator
