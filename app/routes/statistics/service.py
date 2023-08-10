from app.model.employee import EmployeeModel
from dataclasses import dataclass
from decimal import Decimal
from collections import defaultdict
from typing import Any


@dataclass(frozen=True, order=True)
class StatisticsService:

    @staticmethod
    def get_employees_overall_performance() -> dict[str, Any]:
        return {employee.full_name: employee.get_performance_average() for employee in EmployeeModel.query.all()}

    @staticmethod
    def get_best_and_worst_performing_employees() -> Any:
        employees = EmployeeModel.query.all()
        if not employees:
            return {}
        employee_scores = {e.id: e.get_performance_average() for e in employees}
        max_score, min_score = max(employee_scores.values()), min(employee_scores.values())
        return {
            'max': [employee.to_dict() for employee in employees if employee_scores[employee.id] == max_score],
            'min': [employee.to_dict() for employee in employees if employee_scores[employee.id] == min_score],
        }

    @staticmethod
    def get_department_performance_overview() -> dict[str, Any]:
        departments_performance = defaultdict(list)
        for employee in EmployeeModel.query.all():
            departments_performance[employee.department].append(employee.get_performance_average())
        return {department: sum(scores)/len(scores) for department, scores in departments_performance.items()}

    @staticmethod
    def get_employees_salary_average_mean() -> float:
        salaries = [employee.salary for employee in EmployeeModel.query.all()]
        return sum(salaries) / len(salaries)

    @staticmethod
    def get_employees_with_highest_and_lowest_salary() -> Any:
        if not (employees := EmployeeModel.query.all()):
            return None
        max_salary = max(employees, key=lambda x: getattr(x, 'salary')).salary
        min_salary = min(employees, key=lambda x: getattr(x, 'salary')).salary
        return {
            'max': [employee.to_dict() for employee in employees if getattr(employee, 'salary') == max_salary],
            'min': [employee.to_dict() for employee in employees if getattr(employee, 'salary') == min_salary]
        }

    @staticmethod
    def get_department_employee_salary_overview() -> dict[str, Decimal]:
        departments_salaries = defaultdict(list)
        for employee in EmployeeModel.query.all():
            departments_salaries[employee.department].append(employee.salary)
        return {department: sum(salaries)/len(salaries) for department, salaries in departments_salaries.items()}
