from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Any
import json


@dataclass
class Loader(ABC):

    @abstractmethod
    def load(self, path: str) -> list[dict[str, Any]]:
        pass


@dataclass
class JsonLoader(Loader):

    def load(self, path: str) -> list[dict[str, Any]]:
        if not path.endswith('.json'):
            raise AttributeError('Incorrect file extension.')
        try:
            with open(path, 'r', encoding='utf-8') as json_data:
                return json.load(json_data, parse_int=str, parse_float=str)
        except Exception as e:
            raise FileNotFoundError(f'File not found: {e}.')