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
class ProxyEmployeeRepository(Repository):
    employee_repository: Repository
    company_repository: Repository
    fetch_type: FetchType

    def set_fetch_type(self, new_fetch_type: FetchType) -> None:
        self.fetch_type = new_fetch_type

    def find_all(self) -> list[Any]:
        employees = self.employee_repository.find_all()
        if self.fetch_type == FetchType.LAZY:
            return employees
        return [self._get_employee_with_company_data(employee, self.company_repository) for employee in employees]

    def find_by_id(self, id_: int) -> Optional[Any]:
        result = self.employee_repository.find_by_id(id_)
        if self.fetch_type == FetchType.LAZY:
            return result
        return self._get_employee_with_company_data(result, self.company_repository) if result else None

    def add_or_update(self, record: Employee) -> None:
        self.employee_repository.add_or_update(record)

    def delete(self, id_: int) -> None:
        self.employee_repository.delete(id_)

    @staticmethod
    def _get_employee_with_company_data(employee: Employee, company_repo: Repository) -> Employee:
        new_employee_data = employee.to_dict() | {'company': company_repo.find_by_id(employee.company)}
        return Employee.from_dict(new_employee_data)
