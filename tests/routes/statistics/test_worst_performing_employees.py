from app.db.configuration import sa
from app.model.employee import EmployeeModel
from flask.testing import FlaskClient
from flask import Flask


class TestWorstPerformingEmployees:

    def test_when_no_data_available(self, client: FlaskClient, app: Flask) -> None:
        with app.app_context():
            sa.session.query(EmployeeModel).delete()
            sa.session.commit()

        response = client.get('/statistics/employees/worst')

        assert 200 == response.status_code
        assert not response.json

    def test_when_data_available(self, client: FlaskClient, app: Flask) -> None:
        response = client.get('/statistics/employees/worst')

        with app.app_context():
            employees = sa.session.query(EmployeeModel).all()
            min_score = min([e.get_performance_average() for e in employees])
            expected = [e.to_dict() for e in employees if e.get_performance_average() == min_score]

        assert 200 == response.status_code
        assert expected == response.json
