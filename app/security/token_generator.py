from app.model.user import UserModel
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Any
import jwt


@dataclass(frozen=True, order=True)
class AuthorizationTokenGenerator:
    username: str
    role: str
    token_config: dict[str, Any]

    def generate_tokens(self) -> tuple[str, str]:
        access_token_exp = self._get_expiration_date(self.token_config['JWT_AUTHMAXAGE'])
        refresh_token_exp = self._get_expiration_date(self.token_config['JWT_REFRESHMAXAGE'])
        base_token_payload = self._get_base_payload()

        access_token_payload = base_token_payload | {'exp': access_token_exp}
        refresh_token_payload = base_token_payload | {'exp': refresh_token_exp, 'access_token_exp': access_token_exp}

        return self._build_token(access_token_payload), self._build_token(refresh_token_payload)

    def _get_base_payload(self) -> dict[str, Any]:
        return {'iat': datetime.utcnow(), 'sub': self.username, 'role': self.role}

    def _build_token(self, token_payload: dict[str, Any]) -> str:
        return jwt.encode(token_payload, self.token_config['JWT_SECRET'], algorithm=self.token_config['JWT_AUTHTYPE'])

    @staticmethod
    def _get_expiration_date(token_lifespan: int) -> int:
        return int((datetime.utcnow() + timedelta(minutes=token_lifespan)).timestamp())
