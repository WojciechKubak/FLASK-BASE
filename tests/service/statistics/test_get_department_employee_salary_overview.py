from app.model.employee import EmployeeModel
from app.service.statistics import StatisticsService
from app.db.configuration import sa
from flask import Flask


class TestDepartmentEmployeeSalaryOvierview:
    statistics_service = StatisticsService()

    def test_when_no_data_available(self, app: Flask) -> None:
        with app.app_context():
            sa.session.query(EmployeeModel).delete()
            sa.session.commit()

            assert not self.statistics_service.get_department_employee_salary_overview()

    def test_when_data_available(self, app: Flask) -> None:
        with app.app_context():
            employees = sa.session.query(EmployeeModel).all()

            expected = {}
            for department in set([e.department for e in employees]):
                salaries = [e.salary for e in employees if e.department == department]
                expected[department] = sum(salaries) / len(salaries)

            assert expected == self.statistics_service.get_department_employee_salary_overview()
