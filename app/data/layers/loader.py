from dataclasses import dataclass
from abc import ABC, abstractmethod
from itertools import chain
from typing import Any
import json
import os


@dataclass
class Loader(ABC):
    """
    Abstract base class for data loaders.

    Attributes:
        path (str): The path to the directory containing data files.
    """

    path: str

    @abstractmethod
    def load(self) -> list[dict[str, Any]]:
        """
        Abstract method to be implemented by subclasses.

        Returns:
            list[dict[str, Any]]: A list of dictionaries representing the loaded data.
        """
        pass


@dataclass
class JsonLoader(Loader):
    """
    Data loader for JSON files.

    Attributes:
        path (str): The path to the directory containing JSON data files.
    """

    def load(self) -> list[dict[str, Any]]:
        """
        Load data from all JSON files in the specified directory.

        Returns:
            list[dict[str, Any]]: A list of dictionaries representing the loaded data.

        Raises:
            NotADirectoryError: If the provided path is not a directory.
            FileNotFoundError: If there is an error during file loading.
        """
        if not os.path.isdir(self.path):
            raise NotADirectoryError(f'Path {self.path} is not a directory.')
        loaded = [self._load_json_file(f'{self.path}/{file}') for file in os.listdir(self.path)
                  if file.endswith('.json')]
        return list(chain(*loaded))

    @staticmethod
    def _load_json_file(filepath: str) -> list[dict[str, Any]]:
        """
        Load data from a single JSON file.

        Args:
            filepath (str): The path to the JSON file.

        Returns:
            list[dict[str, Any]]: A list of dictionaries representing the loaded data.

        Raises:
            FileNotFoundError: If the file cannot be found or there is an error during loading.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as json_data:
                return json.load(json_data, parse_int=str, parse_float=str)
        except Exception as e:
            raise FileNotFoundError(f'Error occurred: {e}.')
