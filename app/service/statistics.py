from app.model.employee import EmployeeModel
from dataclasses import dataclass
from collections import defaultdict
from decimal import Decimal
from typing import Any


@dataclass(frozen=True, order=True)
class StatisticsService:
    """
    Service class for calculating statistics related to employees.
    """

    def get_employees_overall_performance(self) -> dict[str, Any]:
        """
        Retrieves the overall performance scores of all employees.

        Returns:
            dict[str, Any]: A dictionary where keys are employee full names and values are their performance averages.
        """
        return {employee.full_name: employee.get_performance_average() for employee in EmployeeModel.query.all()}

    def get_best_or_worst_performing_employees(self, best: bool = True) -> list[EmployeeModel]:
        """
        Retrieves a list of the best or worst performing employees.

        Args:
            best (bool, optional): If True, retrieves the best performing employees; otherwise, retrieves
            the worst performing employees. Defaults to True.

        Returns:
            list[EmployeeModel]: A list of EmployeeModel objects representing the best or worst performing employees.
        """
        if not (employees := EmployeeModel.query.all()):
            return []
        grouped_employees_by_performance = defaultdict(list)
        for employee in employees:
            grouped_employees_by_performance[employee.get_performance_average()].append(employee)
        key = max(grouped_employees_by_performance) if best else min(grouped_employees_by_performance)
        return grouped_employees_by_performance[key]

    def get_employees_salary_average_mean(self) -> Decimal:
        """
        Calculates the average salary of all employees.

        Returns:
            Decimal: The average salary.
        """
        if not (employees := EmployeeModel.query.all()):
            return Decimal('0')
        salaries = [employee.salary for employee in employees]
        return sum(salaries) / len(salaries)

    def get_department_performance_overview(self) -> dict[str, Any]:
        """
        Retrieves an overview of department-wise performance scores.

        Returns:
            dict[str, Any]: A dictionary where keys are department names and values are department-wise
            average performance scores.
        """
        if not (employees := EmployeeModel.query.all()):
            return {}
        departments_performance = defaultdict(list)
        for employee in employees:
            departments_performance[employee.department].append(employee.get_performance_average())
        return {department: sum(scores)/len(scores) for department, scores in departments_performance.items()}

    def get_department_employee_salary_overview(self) -> dict[str, Decimal]:
        """
        Retrieves an overview of department-wise average employee salaries.

        Returns:
            dict[str, Decimal]: A dictionary where keys are department names and values are department-wise
            average employee salaries.
        """
        if not (employees := EmployeeModel.query.all()):
            return {}
        departments_salaries = defaultdict(list)
        for employee in employees:
            departments_salaries[employee.department].append(employee.salary)
        return {department: sum(salaries)/len(salaries) for department, salaries in departments_salaries.items()}

    def get_employees_with_highest_or_lowest_salary(self, highest: bool = True) -> list[EmployeeModel]:
        """
        Retrieves a list of employees with the highest or lowest salaries.

        Args:
            highest (bool, optional): If True, retrieves employees with the highest salaries; otherwise, retrieves
            employees with the lowest salaries. Defaults to True.

        Returns:
            list[EmployeeModel]: A list of EmployeeModel objects representing the employees with the
            highest or lowest salaries.
        """
        if not (employees := EmployeeModel.query.all()):
            return []
        grouped_employees_by_salary = defaultdict(list)
        for employee in employees:
            grouped_employees_by_salary[employee.salary].append(employee)
        key = max(grouped_employees_by_salary) if highest else min(grouped_employees_by_salary)
        return grouped_employees_by_salary[key]
