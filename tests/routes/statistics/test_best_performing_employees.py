from app.db.configuration import sa
from app.model.employee import EmployeeModel
from flask.testing import FlaskClient
from flask import Flask
import json


class TestBestPerformingEmployees:

    def test_when_no_data_available(self, client: FlaskClient, app: Flask) -> None:
        with app.app_context():
            sa.session.query(EmployeeModel).delete()
            sa.session.commit()

        response = client.get('/statistics/employees/best')

        assert 200 == response.status_code
        assert not response.json

    def test_when_data_available(self, client: FlaskClient, app: Flask) -> None:
        response = client.get('/statistics/employees/best')

        with app.app_context():
            employees = sa.session.query(EmployeeModel).all()
            max_score = max([e.get_performance_average() for e in employees])
            expected = [e.to_dict() for e in employees if e.get_performance_average() == max_score]

        assert 200 == response.status_code
        assert expected == response.json
