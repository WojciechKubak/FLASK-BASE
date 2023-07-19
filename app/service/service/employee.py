from app.service.repository.repository import Repository
from app.data.model.employee import Employee
from app.service.additional.exporter import DataExporter, FileExportFormat
from dataclasses import dataclass
from typing import Optional, Any, Callable
from decimal import Decimal
from collections import defaultdict


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

    def filter_by(self, criterion: tuple[str, Callable[[Any], bool]]) -> list[Employee]:
        return [employee for employee in self.employee_repository.find_all() if employee.filter_by_criterion(criterion)]

    def get_employees_overall_performance(self) -> dict[int, float]:
        return {employee.id_: employee.get_performance_average() for employee in self.employee_repository.find_all()}

    def get_best_and_worst_performing_employees(self) -> tuple[Employee, Employee]:
        employee_scores = {employee.id_: employee.get_performance_average()
                           for employee in self.employee_repository.find_all()}
        max_ = max(employee_scores, key=employee_scores.get)
        min_ = min(employee_scores, key=employee_scores.get)
        return self.find_by_id(max_), self.find_by_id(min_)

    def get_department_performance_overview(self) -> dict[str, float]:
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

    def export_data(self, path: str, export_type: FileExportFormat) -> None:
        DataExporter().export(self.find_all(), path, export_type)
