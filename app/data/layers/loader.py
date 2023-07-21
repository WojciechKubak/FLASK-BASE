from dataclasses import dataclass
from abc import ABC, abstractmethod
from itertools import chain
from typing import Any
import json
import os


@dataclass
class Loader(ABC):
    path: str

    @abstractmethod
    def load(self) -> list[dict[str, Any]]:
        pass


@dataclass
class JsonLoader(Loader):

    def load(self) -> list[dict[str, Any]]:
        if not os.path.isdir(self.path):
            raise NotADirectoryError(f'Path {self.path} is not a directory.')
        loaded = [self.load_json_file(f'{self.path}/{file}') for file in os.listdir(self.path)
                  if file.endswith('.json')]
        return list(chain(*loaded))

    @staticmethod
    def load_json_file(filepath: str) -> list[dict[str, Any]]:
        try:
            with open(filepath, 'r', encoding='utf-8') as json_data:
                return json.load(json_data, parse_int=str, parse_float=str)
        except Exception as e:
            raise FileNotFoundError(f'Error occurred: {e}.')
