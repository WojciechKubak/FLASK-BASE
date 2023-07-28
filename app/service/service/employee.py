from app.service.repository.repository import Repository
from app.data.model.employee import Employee
from app.service.additional.exporter import DataExporter, FileExportFormat
from dataclasses import dataclass
from typing import Any, Callable
from decimal import Decimal
from collections import defaultdict


@dataclass
class EmployeeService:
    """
    Service class for managing Employee data and performing various operations on it.

    Attributes:
        employee_repository (Repository): The repository instance for Employee data.
    """

    employee_repository: Repository

    def find_all(self) -> list[Any]:
        """
        Retrieve all Employee records from the repository.

        Returns:
            list[Any]: A list of all Employee records in the repository.
        """
        return self.employee_repository.find_all()

    def find_by_id(self, id_: int) -> Any:
        """
        Retrieve an Employee record from the repository based on its ID.

        Args:
            id_ (int): The ID of the Employee record to retrieve.

        Returns:
            Any: The Employee record if found, otherwise None.
        """
        if id_ < 0:
            raise ValueError('Id must be non-negative number.')
        return self.employee_repository.find_by_id(id_)

    def add_or_update(self, record: Any) -> None:
        """
        Add or update an Employee record in the repository.

        Args:
            record (Any): The Employee record to add or update.
        """
        self.employee_repository.add_or_update(record)

    def delete(self, id_: int) -> None:
        """
        Delete an Employee record from the repository based on its ID.

        Args:
            id_ (int): The ID of the Employee record to delete.
        """
        if id_ < 0:
            raise ValueError('Id must be non-negative number.')
        self.employee_repository.delete(id_)

    def filter_by(self, criterion: tuple[str, Callable[[Any], bool]]) -> list[Employee]:
        """
        Filter Employee records based on a given criterion.

        Args:
            criterion (tuple[str, Callable[[Any], bool]]): A tuple containing the attribute name and
            the filtering condition as a callable function.

        Returns:
            list[Employee]: A list of Employee records that satisfy the given criterion.
        """
        return [employee for employee in self.employee_repository.find_all() if employee.filter_by_criterion(criterion)]

    def get_employees_overall_performance(self) -> dict[int, float]:
        """
        Get the overall performance average for each Employee.

        Returns:
            dict[int, float]: A dictionary containing Employee IDs as keys and their overall performance average as values.
        """
        return {employee.id_: employee.get_performance_average() for employee in self.employee_repository.find_all()}

    def get_best_and_worst_performing_employees(self) -> dict[str, list[Employee]]:
        """
        Get the best and worst performing Employees based on their performance average.

        Returns:
            dict[str, list[Employee]]: A dictionary containing lists of best and worst performing Employees.
                                       The keys are "max" and "min", and the values are lists of Employees.
                                       Employees with the same highest and lowest performance scores will be
                                       grouped together in the corresponding lists.
        """
        employees = self.employee_repository.find_all()
        employee_scores = {e.id_: e.get_performance_average() for e in employees}
        max_score, min_score = max(employee_scores.values()), min(employee_scores.values())
        return {
            'max': [employee for employee in employees if employee_scores[employee.id_] == max_score],
            'min': [employee for employee in employees if employee_scores[employee.id_] == min_score],
        }

    def get_department_performance_overview(self) -> dict[str, float]:
        """
        Get the performance average for each department.

        Returns:
            dict[str, float]: A dictionary containing department names as keys and their performance average as values.
        """
        departments_performance = defaultdict(list)
        for employee in self.employee_repository.find_all():
            departments_performance[employee.department].append(employee.get_performance_average())
        return {department: sum(scores)/len(scores) for department, scores in departments_performance.items()}

    def get_employees_salary_average_mean(self) -> Decimal:
        """
        Get the average mean of Employee salaries.

        Returns:
            Decimal: The average mean of Employee salaries.
        """
        salaries = [employee.salary for employee in self.employee_repository.find_all()]
        return sum(salaries) / len(salaries)

    def get_employees_with_highest_and_lowest_salary(self) -> tuple[Employee, Employee]:
        """
        Get the Employees with the highest and lowest salaries.

        Returns:
            tuple[Employee, Employee]: A tuple containing the Employee with the highest and lowest salaries.
        """
        employees = self.employee_repository.find_all()
        max_ = max(employees, key=lambda x: getattr(x, 'salary'))
        min_ = min(employees, key=lambda x: getattr(x, 'salary'))
        return max_, min_

    def get_department_employee_salary_overview(self) -> dict[str, Decimal]:
        """
        Get the salary overview for each department.

        Returns:
            dict[str, Decimal]: A dictionary containing department names as keys and their salary overview as values.
        """
        departments_salaries = defaultdict(list)
        for employee in self.employee_repository.find_all():
            departments_salaries[employee.department].append(employee.salary)
        return {department: sum(salaries)/len(salaries) for department, salaries in departments_salaries.items()}

    def export_data(self, path: str, export_type: FileExportFormat) -> None:
        """
        Export Employee data to a specified file path in the desired export format.

        Args:
            path (str): The file path where the data will be exported.
            export_type (FileExportFormat): The export format (TXT_FILE or JSON_FILE) for the data.
        """
        DataExporter().export(self.find_all(), path, export_type)
