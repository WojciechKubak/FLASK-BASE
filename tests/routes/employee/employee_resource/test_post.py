from app.model.employee import EmployeeModel
from app.db.configuration import sa
from flask.testing import FlaskClient
from flask import Flask
from typing import Any


class TestEmployeeResourcePost:

    def test_when_added(self, client: FlaskClient, app: Flask, employee_model_data: dict[str, Any]) -> None:
        response = client.post(f"employees/{employee_model_data.pop('full_name')}", json=employee_model_data)

        assert 201 == response.status_code

        with app.app_context():
            assert sa.session.query(EmployeeModel).first().to_dict() == response.json

    def test_when_employee_exists(self, client: FlaskClient, app: Flask, employee_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(EmployeeModel(**employee_model_data))
            sa.session.commit()

        response = client.post(f"employees/{employee_model_data['full_name']}", json=employee_model_data)

        assert 400 == response.status_code
        assert b'Employee already exists' in response.data

    def test_when_company_id_not_found(self, client: FlaskClient) -> None:
        response = client.post('employees/Employee', json={'company_id': 999})

        assert 400 == response.status_code
        assert b'Company id not found' in response.data

    def test_when_validation_error_occurs(self, client: FlaskClient) -> None:
        response = client.post('employees/Employee', json={'company_id': 1})

        assert 400 == response.status_code
        assert b'field required' in response.data
