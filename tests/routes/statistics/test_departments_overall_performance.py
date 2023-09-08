from app.db.configuration import sa
from app.model.employee import EmployeeModel
from flask.testing import FlaskClient
from flask import Flask


class TestDepartmentOverallPerformance:

    def test_when_no_data_available(self, client: FlaskClient, app: Flask) -> None:
        with app.app_context():
            sa.session.query(EmployeeModel).delete()
            sa.session.commit()

        response = client.get('/statistics/departments/performance')

        assert 200 == response.status_code
        assert not response.json

    def test_when_data_available(self, client: FlaskClient, app: Flask) -> None:
        response = client.get('/statistics/departments/performance')

        with app.app_context():
            employees = sa.session.query(EmployeeModel).all()
            expected = {}
            for department in set([e.department for e in employees]):
                scores = [e.get_performance_average() for e in employees if e.department == department]
                expected[department] = sum(scores) / len(scores)

        assert 200 == response.status_code
        assert expected == response.json
