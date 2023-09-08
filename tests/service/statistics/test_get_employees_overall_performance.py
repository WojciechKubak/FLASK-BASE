from app.service.statistics import StatisticsService
from app.model.employee import EmployeeModel
from app.db.configuration import sa
from flask import Flask


def test_get_employees_overall_performance(app: Flask) -> None:
    with app.app_context():
        employees = sa.session.query(EmployeeModel).all()

        result = StatisticsService().get_employees_overall_performance()

        assert {e.full_name: e.get_performance_average() for e in employees} == result
