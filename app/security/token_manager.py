from datetime import datetime, timedelta
from dataclasses import dataclass
from flask import Response, make_response
from typing import Any
import jwt
import os


@dataclass
class TokenManager:

    def __post_init__(self):
        self.token_config = {
            'JWT_AUTHTYPE': os.environ.get('JWT_AUTHTYPE'),
            'JWT_SECRET': os.environ.get('JWT_SECRET'),
            'JWT_AUTHMAXAGE': int(os.environ.get('JWT_AUTHMAXAGE')),
            'JWT_REFRESHMAXAGE': int(os.environ.get('JWT_REFRESHMAXAGE'))
        }

    def generate_response_with_access_tokens(self, username: str, role: str) -> Response:
        access_token, refresh_token = self._get_access_and_refresh_tokens(username, role)
        return self._build_response(access_token, refresh_token)

    def generete_response_with_refreshed_tokens(self, token: str) -> Response:
        token = self.decode_token(token)
        access_token, refresh_token = self._get_access_and_refresh_tokens(token['sub'], token['role'])
        return self._build_response(access_token, refresh_token)

    def encode_token(self, token_payload: dict[str, Any]) -> str:
        return jwt.encode(token_payload, self.token_config['JWT_SECRET'], algorithm=self.token_config['JWT_AUTHTYPE'])

    def decode_token(self, token: str) -> dict[str, Any]:
        return jwt.decode(token, self.token_config['JWT_SECRET'], algorithms=[self.token_config['JWT_AUTHTYPE']])

    def _get_access_and_refresh_tokens(self, username: str, role: str) -> tuple[str, str]:
        access_token_exp = self._get_expiration_date(self.token_config['JWT_AUTHMAXAGE'])
        refresh_token_exp = self._get_expiration_date(self.token_config['JWT_REFRESHMAXAGE'])
        base_token_payload = self._get_base_payload(username, role)

        access_token_payload = base_token_payload | {'exp': access_token_exp}
        refresh_token_payload = base_token_payload | {'exp': refresh_token_exp, 'access_token_exp': access_token_exp}

        return self.encode_token(access_token_payload), self.encode_token(refresh_token_payload)

    @staticmethod
    def _build_response(access_token: str, refresh_token: str) -> Response:
        response_body = {'access': access_token, 'refresh': refresh_token}
        response = make_response(response_body, 201)
        response.set_cookie('access', access_token, httponly=True)
        response.set_cookie('refresh', refresh_token, httponly=True)

        return response

    @staticmethod
    def _get_base_payload(username: str, role: str) -> dict[str, Any]:
        return {'iat': datetime.utcnow(), 'sub': username, 'role': role}

    @staticmethod
    def _get_expiration_date(token_lifespan: int) -> int:
        return int((datetime.utcnow() + timedelta(minutes=token_lifespan)).timestamp())
