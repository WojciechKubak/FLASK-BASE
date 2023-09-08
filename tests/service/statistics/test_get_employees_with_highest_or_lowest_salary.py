from app.model.employee import EmployeeModel
from app.service.statistics import StatisticsService
from app.db.configuration import sa
from flask import Flask


class TestGetEmployeesWithHighestOrLowestSalary:
    statistics_service = StatisticsService()

    def test_when_no_data_available(self, app: Flask) -> None:
        with app.app_context():
            sa.session.query(EmployeeModel).delete()
            sa.session.commit()

            assert not self.statistics_service.get_employees_with_highest_or_lowest_salary()

    def test_with_highest_salaries(self, app: Flask) -> None:
        with app.app_context():
            employees = sa.session.query(EmployeeModel).all()

            max_salary = max([e.salary for e in employees])
            expected = [e for e in employees if e.salary == max_salary]

            assert expected == self.statistics_service.get_employees_with_highest_or_lowest_salary()

    def test_with_lowest_salaries(self, app: Flask) -> None:
        with app.app_context():
            employees = sa.session.query(EmployeeModel).all()

            min_salary = min([e.salary for e in employees])
            expected = [e for e in employees if e.salary == min_salary]

            assert expected == self.statistics_service.get_employees_with_highest_or_lowest_salary(highest=False)
