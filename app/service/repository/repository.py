from app.data.model.employee import Employee
from app.data.model.company import Company
from app.data.factory.processor import DataProcessor, DataFactoryType
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Optional, Any
from enum import Enum, auto


class FetchType(Enum):
    """
    Enumeration of data fetching types.

    Attributes:
        EAGER (FetchType): Represents the eager fetching type.
        LAZY (FetchType): Represents the lazy fetching type.
    """
    EAGER = auto()
    LAZY = auto()


@dataclass
class Repository(ABC):
    """
    Abstract base class for repositories that manage data storage and retrieval.
    """

    @abstractmethod
    def find_all(self) -> list[Any]:
        """
        Retrieve all records from the repository.

        Returns:
            list[Any]: A list of all records in the repository.
        """
        pass

    @abstractmethod
    def find_by_id(self, id_: int) -> Optional[Any]:
        """
        Retrieve a record from the repository based on its ID.

        Args:
            id_ (int): The ID of the record to retrieve.

        Returns:
            Optional[Any]: The record if found, otherwise None.
        """
        pass

    @abstractmethod
    def add_or_update(self, record: Any) -> None:
        """
        Add or update a record in the repository.

        Args:
            record (Any): The record to add or update.
        """
        pass

    @abstractmethod
    def delete(self, id_: int) -> None:
        """
        Delete a record from the repository based on its ID.

        Args:
            id_ (int): The ID of the record to delete.
        """
        pass


@dataclass
class CompanyRepository(Repository):
    """
    Repository class for managing Company data.

    Attributes:
        path (str): The path to the directory containing JSON files.
        constraints (dict[str, Any]): Dictionary of validation constraints for the data.
        companies (list[Company]): List of Company objects stored in the repository.
    """

    path: str
    constraints: dict[str, Any]
    companies: list[Company] = field(default_factory=list, init=False)

    def __post_init__(self):
        """
        Initialize the repository after creating an instance.
        Loads and processes the Company data using DataProcessor.
        """
        self.companies = DataProcessor.create_processor(
            DataFactoryType.COMPANY_FACTORY,
            self.path,
            self.constraints
        ).process()

    def find_all(self) -> list[Company]:
        """
        Retrieve all Company records from the repository.

        Returns:
            list[Company]: A list of all Company records in the repository.
        """
        return self.companies

    def find_by_id(self, id_: int) -> Optional[Company]:
        """
        Retrieve a Company record from the repository based on its ID.

        Args:
            id_ (int): The ID of the Company record to retrieve.

        Returns:
            Optional[Company]: The Company record if found, otherwise None.
        """
        if filtered := [company for company in self.companies if company.id_ == id_]:
            return filtered[0]
        return None

    def add_or_update(self, record: Company) -> None:
        """
        Add or update a Company record in the repository.

        Args:
            record (Company): The Company record to add or update.
        """
        if filtered_companies := [company for company in self.companies if company.id_ == record.id_]:
            self.companies.remove(filtered_companies[0])
        self.companies.append(record)

    def delete(self, id_: int) -> None:
        """
        Delete a Company record from the repository based on its ID.

        Args:
            id_ (int): The ID of the Company record to delete.
        """
        self.companies = [company for company in self.companies if company.id_ != id_]


@dataclass
class EmployeeRepository(Repository):
    """
    Repository class for managing Employee data.

    Attributes:
        path (str): The path to the directory containing JSON files.
        constraints (dict[str, Any]): Dictionary of validation constraints for the data.
        employees (list[Employee]): List of Employee objects stored in the repository.
    """

    path: str
    constraints: dict[str, Any]
    employees: list[Employee] = field(default_factory=list, init=False)

    def __post_init__(self):
        """
        Initialize the repository after creating an instance.
        Loads and processes the Employee data using DataProcessor.
        """
        self.employees = DataProcessor.create_processor(
            DataFactoryType.EMPLOYEE_FACTORY,
            self.path,
            self.constraints
        ).process()

    def find_all(self) -> list[Employee]:
        """
        Retrieve all Employee records from the repository.

        Returns:
            list[Employee]: A list of all Employee records in the repository.
        """
        return self.employees

    def find_by_id(self, id_: int) -> Optional[Employee]:
        """
        Retrieve an Employee record from the repository based on its ID.

        Args:
            id_ (int): The ID of the Employee record to retrieve.

        Returns:
            Optional[Employee]: The Employee record if found, otherwise None.
        """
        if filtered := [employee for employee in self.employees if employee.id_ == id_]:
            return filtered[0]
        return None

    def add_or_update(self, record: Employee) -> None:
        """
        Add or update an Employee record in the repository.

        Args:
            record (Employee): The Employee record to add or update.
        """
        if filtered_employees := [employee for employee in self.employees if employee.id_ == record.id_]:
            self.employees.remove(filtered_employees[0])
        self.employees.append(record)

    def delete(self, id_: int) -> None:
        """
        Delete an Employee record from the repository based on its ID.

        Args:
            id_ (int): The ID of the Employee record to delete.
        """
        self.employees = [employee for employee in self.employees if employee.id_ != id_]


@dataclass
class ProxyCompanyRepository(Repository):
    """
    Proxy repository class for managing Company data with optional lazy loading of Employee data.

    Attributes:
        company_repository (CompanyRepository): The actual Company repository instance.
        employee_repository (EmployeeRepository): The Employee repository instance.
        fetch_type (FetchType): The data fetching type (eager or lazy).
    """

    company_repository: CompanyRepository
    employee_repository: EmployeeRepository
    fetch_type: FetchType

    def set_fetch_type(self, new_fetch_type: FetchType) -> None:
        """
        Set the data fetching type for the repository.

        Args:
            new_fetch_type (FetchType): The new data fetching type.
        """
        self.fetch_type = new_fetch_type

    def find_all(self) -> list[Any]:
        """
        Retrieve all Company records from the repository with optional lazy-loaded Employee data.

        Returns:
            list[Any]: A list of all Company records in the repository.
        """
        return [ProxyCompanyRepository._get_employee_data(
            company, self.employee_repository, only_id=self.fetch_type == FetchType.LAZY)
            for company in self.company_repository.find_all()]

    def find_by_id(self, id_: int) -> Any:
        """
        Retrieve a Company record from the repository based on its ID with optional lazy-loaded Employee data.

        Args:
            id_ (int): The ID of the Company record to retrieve.

        Returns:
            Any: The Company record with optional lazy-loaded Employee data if found, otherwise None.
        """
        result = self.company_repository.find_by_id(id_)
        return self._get_employee_data(result, self.employee_repository, only_id=self.fetch_type == FetchType.LAZY) \
            if result else None

    def add_or_update(self, record: Any) -> None:
        """
        Add or update a Company record in the repository.

        Args:
            record (Any): The Company record to add or update.
        """
        self.company_repository.add_or_update(record)

    def delete(self, id_: int) -> None:
        """
        Delete a Company record from the repository based on its ID.

        Args:
            id_ (int): The ID of the Company record to delete.
        """
        self.company_repository.delete(id_)

    @staticmethod
    def _get_employee_data(company: Company, employees_repository: EmployeeRepository, only_id: bool = True) -> Company:
        """
        Get Company data with optional lazy-loaded Employee data.

        Args:
            company (Company): The Company object.
            employees_repository (EmployeeRepository): The Employee repository instance.
            only_id (bool, optional): If True, only the IDs of employees are included, otherwise full Employee objects.

        Returns:
            Company: The Company object with Employee data.
        """
        employees = [e.id_ if only_id else e for e in employees_repository.find_all() if e.company == company.id_]
        return Company.from_dict(company.to_dict() | {'employees': employees})
