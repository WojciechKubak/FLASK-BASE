from app.data.model.employee import Employee
from app.data.model.company import Company
from app.data.factory.processor import DataProcessor, DataFactoryType
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Optional, Any
from enum import Enum, auto


class FetchType(Enum):
    EAGER = auto()
    LAZY = auto()


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

    def find_by_id(self, id_: int) -> Any:
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
class EmployeeRepository(Repository):
    path: str
    constraints: dict[str, Any]
    employees: list[Employee] = field(default_factory=list, init=False)

    def __post_init__(self):
        self.employees = DataProcessor.create_processor(
            DataFactoryType.EMPLOYEE_FACTORY,
            self.path,
            self.constraints
        ).process()

    def find_all(self) -> list[Any]:
        return self.employees

    def find_by_id(self, id_: int) -> Optional[Any]:
        if filtered := [employee for employee in self.employees if employee.id_ == id_]:
            return filtered[0]
        return None

    def add_or_update(self, record: Any) -> None:
        if filtered_employees := [employee for employee in self.employees if employee.id_ == record.id_]:
            self.employees.remove(filtered_employees[0])
        self.employees.append(record)

    def delete(self, id_: int) -> None:
        self.employees = [employee for employee in self.employees if employee.id_ != id_]


@dataclass
class ProxyCompanyRepository(Repository):
    company_repository: CompanyRepository
    employee_repository: EmployeeRepository
    fetch_type: FetchType

    def set_fetch_type(self, new_fetch_type: FetchType) -> None:
        self.fetch_type = new_fetch_type

    def find_all(self) -> list[Any]:
        return [ProxyCompanyRepository.get_employee_data(
            company, self.employee_repository, only_id=self.fetch_type == FetchType.LAZY)
            for company in self.company_repository.find_all()]

    def find_by_id(self, id_: int) -> Any:
        result = self.company_repository.find_by_id(id_)
        if self.fetch_type == FetchType.LAZY:
            return result
        return self.get_employees(result, self.employee_repository) if result else None

    def add_or_update(self, record: Any) -> None:
        self.company_repository.add_or_update(record)

    def delete(self, id_: int) -> None:
        self.company_repository.delete(id_)

    @staticmethod
    def get_employee_data(company: Company, employees_repository: EmployeeRepository, only_id: bool = True) -> Company:
        employees = [e.id_ if only_id else e for e in employees_repository.find_all() if e.company == company.id_]
        return Company.from_dict(company.to_dict() | {'employees': employees})
