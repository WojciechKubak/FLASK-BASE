from app.model.employee import EmployeeModel
from app.db.configuration import sa
from flask.testing import FlaskClient
from flask import Flask
from typing import Any


class TestEmployeeResourceDelete:

    def test_when_deleted(self, client: FlaskClient, app: Flask, employee_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(EmployeeModel(**employee_model_data))
            sa.session.commit()

        response = client.delete(f"/employees/{employee_model_data['full_name']}")

        assert 200 == response.status_code
        assert b'Deleted employee with id' in response.data

    def test_when_employee_does_not_exist(self, client: FlaskClient) -> None:
        response = client.delete('/employees/Employee')

        assert 400 == response.status_code
        assert b'Employee not found' in response.data
