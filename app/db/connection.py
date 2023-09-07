from dataclasses import dataclass
from typing import Any, Self


@dataclass
class ConnectionPoolBuilder:
    params: dict[str, Any]

    def __post_init__(self):
        self._pool_config = {
            'host': 'localhost',
            'database': 'db_1',
            'user': 'user',
            'password': 'user1234',
            'port': 3307
        } | self.params

    def set_host(self, new_host: str) -> Self:
        self._pool_config['host'] = new_host
        return self

    def set_database(self, new_database: str) -> Self:
        self._pool_config['database'] = new_database
        return self

    def set_user(self, new_user: str) -> Self:
        self._pool_config['user'] = new_user
        return self

    def set_password(self, new_password: str) -> Self:
        self._pool_config['password'] = new_password
        return self

    def set_port(self, new_port: int) -> Self:
        self._pool_config['port'] = new_port
        return self

    def build_connection_string(self) -> str:
        return f"mysql://{self._pool_config['user']}:{self._pool_config['password']}" \
               f"@{self._pool_config['host']}:{self._pool_config['port']}/{self._pool_config['database']}"

    @classmethod
    def builder(cls: Self, params: dict[str, Any] = None) -> Self:
        return cls(params if params else {})
