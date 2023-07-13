from app.service.additionals.repository import Repository
from app.data.factory.processor import DataProcessor, DataFactoryType
from app.data.model.company import Company
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class CompanyRepository(Repository):
    path: str
    constraints: dict[str, Any]
    companies: list[Company] = field(default_factory=list, init=False)

    def __post_init__(self):
        self.companies = DataProcessor.create_processor(
            DataFactoryType.COMPANY_FACTORY,
            self.path,
            self.constraints
        ).process()

    def find_all(self) -> list[Any]:
        return self.companies

    def find_by_id(self, id_: int) -> Optional[Any]:
        if filtered := [company for company in self.companies if company.id_ == id_]:
            return filtered[0]
        return None

    def add_or_update(self, record: Any) -> None:
        if filtered_companies := [company for company in self.companies if company.id_ == record.id_]:
            self.companies.remove(filtered_companies[0])
        self.companies.append(record)

    def delete(self, id_: int) -> None:
        self.companies = [company for company in self.companies if company.id_ != id_]


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



