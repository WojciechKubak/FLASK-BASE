from app.model.employee import EmployeeModel
from dataclasses import dataclass
from collections import defaultdict
from decimal import Decimal
from typing import Any


@dataclass(frozen=True, order=True)
class StatisticsService:

    def get_employees_overall_performance(self) -> dict[str, Any]:
        return {employee.full_name: employee.get_performance_average() for employee in EmployeeModel.query.all()}

    def get_best_or_worst_performing_employees(self, best: bool = True) -> list[EmployeeModel]:
        grouped_employees_by_performance = defaultdict(list)
        for employee in EmployeeModel.query.all():
            grouped_employees_by_performance[employee.get_performance_average()].append(employee)
        key = max(grouped_employees_by_performance) if best else min(grouped_employees_by_performance)
        return grouped_employees_by_performance[key]

    def get_employees_salary_average_mean(self) -> Decimal:
        salaries = [employee.salary for employee in EmployeeModel.query.all()]
        return sum(salaries) / len(salaries)

    def get_department_performance_overview(self) -> dict[str, Any]:
        departments_performance = defaultdict(list)
        for employee in EmployeeModel.query.all():
            departments_performance[employee.department].append(employee.get_performance_average())
        return {department: sum(scores)/len(scores) for department, scores in departments_performance.items()}

    def get_department_employee_salary_overview(self) -> dict[str, Decimal]:
        departments_salaries = defaultdict(list)
        for employee in EmployeeModel.query.all():
            departments_salaries[employee.department].append(employee.salary)
        return {department: sum(salaries)/len(salaries) for department, salaries in departments_salaries.items()}

    def get_employees_with_highest_or_lowest_salary(self, highest: bool = True) -> list[EmployeeModel]:
        grouped_employees_by_salary = defaultdict(list)
        for employee in EmployeeModel.query.all():
            grouped_employees_by_salary[employee.salary].append(employee)
        key = max(grouped_employees_by_salary) if highest else min(grouped_employees_by_salary)
        return grouped_employees_by_salary[key]
