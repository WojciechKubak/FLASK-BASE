from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional, Any


@dataclass
class Repository(ABC):

    @abstractmethod
    def find_all(self) -> list[Any]:
        pass

    @abstractmethod
    def find_by_id(self, id_: int) -> Optional[Any]:
        pass

    @abstractmethod
    def add_or_update(self, record: Any) -> None:
        pass

    @abstractmethod
    def delete(self, id_: int) -> None:
        pass
