from app.service.repository.repository import Repository
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class CompanyService:
    company_repository: Repository

    def find_all(self) -> list[Any]:
        return self.company_repository.find_all()

    def find_by_id(self, id_: int) -> Optional[Any]:
        if id_ < 0:
            raise ValueError('Id must be non-negative number.')
        return self.company_repository.find_by_id(id_)

    def add_or_update(self, record: Any) -> None:
        self.company_repository.add_or_update(record)

    def delete(self, id_: int) -> None:
        if id_ < 0:
            raise ValueError('Id must be non-negative number.')
        self.company_repository.delete(id_)



