from app.model.employee import EmployeeModel
from app.service.statistics import StatisticsService
from app.db.configuration import sa
from flask import Flask


class TestGetBestAndWorstPerformingEmployees:
    statistics_service = StatisticsService()

    def test_when_no_data_available(self, app: Flask) -> None:
        with app.app_context():
            sa.session.query(EmployeeModel).delete()
            sa.session.commit()

            assert not self.statistics_service.get_best_or_worst_performing_employees()

    def test_when_getting_best_employees(self, app: Flask) -> None:
        with app.app_context():
            employees = sa.session.query(EmployeeModel).all()

            result = self.statistics_service.get_best_or_worst_performing_employees()

            best_score = max([e.get_performance_average() for e in employees])
            expected = [e for e in employees if e.get_performance_average() == best_score]

            assert expected == result

    def test_when_getting_worst_employees(self, app: Flask) -> None:
        with app.app_context():
            employees = sa.session.query(EmployeeModel).all()

            result = self.statistics_service.get_best_or_worst_performing_employees(best=False)

            worst_score = min([e.get_performance_average() for e in employees])
            expected = [e for e in employees if e.get_performance_average() == worst_score]

            assert expected == result
