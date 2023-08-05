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

    def set_config_params(self, params: dict[str, Any]) -> Self:
        available_keys = self.config.keys()
        if not all([k in available_keys for k in params.keys()]):
            raise AttributeError('Parameter name out of pool.')
        self.config = self.config | params
        return self

    def build_connection_string(self) -> str:
        return f"mysql://{self.config['user']}:{self.config['password']}" \
               f"@{self.config['host']}:{self.config['port']}/{self.config['database']}"
