from app.service.additionals.repository import Repository
from app.data.factory.processor import DataProcessor, DataFactoryType
from app.data.organization.employee import Employee
from app.service.additionals.exporter import DataExporter
from dataclasses import dataclass, field
from typing import Optional, Any
from enum import Enum, auto
from decimal import Decimal
from collections import defaultdict

# todo (2):
"""
    Biorąc pod uwagę ostatni todos zrealizowałem kilka zmian dla proxy, ogólnie wyszło, że podstawowe metody
    zrealizowane w klasie ProxyEmployeeRepository spokojnie wystarczą do implementacji wszystkich oczekiwanych metod
    serwisowych. Wprowadzone zmiany:
        1. pojedyńcza klasa Repository (wcześniej po jednej dla Employee i Company),
        2. ładowanie danych na poziomie inicjalizacji obiektu repozytorium (wywołanie factory),
        3. odchudzenie ProxyEmployeeRepository do właściwie wyłącznie metod które muszą być implementowane.
        
    Prosiłbym jeszcze raz o rzucenie na to okiem
    (na ten moment nie testowałem samych metod, chciałem sprawdzić czy te PROXY uda się doprowadzić do końca)
"""


class FetchType(Enum):
    EAGER = auto()
    LAZY = auto()


class FileExportFormat(Enum):
    CSV_FILE = auto()
    TXT_FILE = auto()
    JSON_FILE = auto()


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
        if filtered := [employee for employee in self.employees if employee.id == id_]:
            return filtered[0]
        return None

    def add_or_update(self, record: Any) -> None:
        if filtered_employees := [employee for employee in self.employees if employee.id == record.id]:
            self.employees.remove(filtered_employees[0])
        self.employees.append(record)

    def delete(self, id_: int) -> None:
        self.employees = [employee for employee in self.employees if employee.id != id_]


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
        new_employee_data = employee.__dict__ | {'company_id': company_repo.find_by_id(employee.company_id)}
        return Employee.from_dict(new_employee_data)


@dataclass
class EmployeeService:
    employee_repository: Repository

    def find_all(self) -> list[Any]:
        return self.employee_repository.find_all()

    def find_by_id(self, id_: int) -> Optional[Any]:
        if id_ < 0:
            raise ValueError('Id must be non-negative number.')
        return self.employee_repository.find_by_id(id_)

    def add_or_update(self, record: Any) -> None:
        self.employee_repository.add_or_update(record)

    def delete(self, id_: int) -> None:
        if id_ < 0:
            raise ValueError('Id must be non-negative number.')
        self.employee_repository.delete(id_)

    def filter_by(self, element: dict[str, str]) -> list[Employee]:
        # todo (3): jak zrealizować wyszukiwanie pracownika po wybranym kryterium?
        ...

    def get_employees_overall_performance(self) -> dict[Employee, float]:
        return {employee: employee.get_performance_average() for employee in self.employee_repository.find_all()}

    def get_best_and_worst_performing_employees(self) -> tuple[Employee, Employee]:
        employee_scores = {employee: employee.get_performance_average()
                           for employee in self.employee_repository.find_all()}
        max_ = max(employee_scores, key=lambda x: x[1])
        min_ = min(employee_scores, key=lambda x: x[1])
        return max_, min_

    def get_department_performance_overview(self) -> dict[str, float]:
        # todo (4):
        """
        ze względu na to, że employee_repository jest hintowanie jako Repository, a nie jak wcześniej EmployeeRepository
        to przy próbie wywołania self.employee_repository.employees dostaję 'unresolved attribute' co jest sensowne,
        ponieważ nie ma wyjściowo takiego pola w ABC Repository, rozwiązaniem jest zastąpienie
        self.employee_repository.employees -> self.employee_repository.find_all()
        ale w przypadku takim jak ten, zakładając, że mamy typ EAGER, metoda find_all() dociągnie dane
        o companies, mimo, że i tak nie zostaną tutaj wykorzystane (funkcja zwraca dict[str, float])
        a przekłada się to na dodatkową złożoność która nie musiałaby być realizowana.
        """
        departments_performance = defaultdict(list)
        for employee in self.employee_repository.find_all():
            departments_performance[employee.department].append(employee.get_performance_average())
        return {department: sum(scores)/len(scores) for department, scores in departments_performance.items()}

    def get_employees_salary_average_mean(self) -> Decimal:
        salaries = [employee.salary for employee in self.employee_repository.find_all()]
        return sum(salaries) / len(salaries)

    def get_employees_with_highest_and_lowest_salary(self) -> tuple[Employee, Employee]:
        employees = self.employee_repository.find_all()
        max_ = max(employees, key=lambda x: getattr(x, 'salary'))
        min_ = min(employees, key=lambda x: getattr(x, 'salary'))
        return max_, min_

    def get_department_employee_salary_overview(self) -> dict[str, Decimal]:
        departments_salaries = defaultdict(list)
        for employee in self.employee_repository.find_all():
            departments_salaries[employee.department].append(employee.salary)
        return {department: sum(salaries)/len(salaries) for department, salaries in departments_salaries.items()}

    def export_data(self, export_type: FileExportFormat, path: str) -> None:
        # todo (5): sprawdzenie czy FileExportFormat jest poprawny (dodatkowo czy struktura plików app.service.additional jest poprawna
        # bo wydaje mi się, że repository.py powinno być na innym poziomie.
        match export_type:
            case FileExportFormat.JSON_FILE:
                DataExporter.export_to_json(self.employee_repository.find_all(), path)
            case FileExportFormat.CSV_FILE:
                DataExporter.export_to_json(self.employee_repository.find_all(), path)
            case FileExportFormat.TXT_FILE:
                DataExporter.export_to_json(self.employee_repository.find_all(), path)

