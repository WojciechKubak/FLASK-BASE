from app.service.statistics import StatisticsService
from app.model.employee import EmployeeModel
from app.db.configuration import sa
from flask import Flask


class TestGetDepartmentPerformanceOverview:
    statistics_service = StatisticsService()

    def test_when_no_data_available(self, app: Flask) -> None:
        with app.app_context():
            sa.session.query(EmployeeModel).delete()
            sa.session.commit()

            assert not self.statistics_service.get_department_performance_overview()

    def test_when_data_available(self, app: Flask) -> None:
        with app.app_context():
            employees = sa.session.query(EmployeeModel).all()

            result = self.statistics_service.get_department_performance_overview()

            expected = {}
            for department in set([e.department for e in employees]):
                scores = [e.get_performance_average() for e in employees if e.department == department]
                expected[department] = sum(scores) / len(scores)

            assert expected == result
