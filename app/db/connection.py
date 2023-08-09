from dataclasses import dataclass, field
from typing import Any, Self


@dataclass
class MySQLConnectionPoolBuilder:
    config: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.config:
            self.config = {
                'host': 'localhost',
                'database': 'db_1',
                'user': 'user',
                'password': 'user1234',
                'port': 3307
            }

    def set_host(self, new_host: str) -> Self:
        self.config['host'] = new_host
        return self

    def set_database(self, new_database: str) -> Self:
        self.config['database'] = new_database
        return self

    def set_user(self, new_user: str) -> Self:
        self.config['user'] = new_user
        return self

    def set_password(self, new_password: str) -> Self:
        self.config['password'] = new_password
        return self

    def set_port(self, new_port: int) -> Self:
        self.config['port'] = new_port
        return self

    def build_connection_string(self) -> str:
        return f"mysql://{self.config['user']}:{self.config['password']}" \
               f"@{self.config['host']}:{self.config['port']}/{self.config['database']}"
