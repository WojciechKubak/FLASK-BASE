from app.model.employee import EmployeeModel
from app.db.configuration import sa
from flask.testing import FlaskClient
from flask import Flask
from typing import Any


class TestEmployeeyResourceGet:

    def test_when_employee_exists(self, client: FlaskClient, app: Flask, employee_model_data: dict[str, Any]) -> None:
        with app.app_context():
            employee = EmployeeModel(**employee_model_data)
            sa.session.add(employee)

            response = client.get(f"/employees/{employee_model_data['full_name']}")

            assert 200 == response.status_code
            assert employee.to_dict() == response.json

    def test_when_employee_does_not_exists(self, client: FlaskClient, app: Flask) -> None:
        response = client.get('/employees/Employee')

        assert 400 == response.status_code
        assert b'Employee not found' in response.data
