from app.model.employee import EmployeeModel
from app.db.configuration import sa
from flask.testing import FlaskClient
from flask import Flask
from typing import Any


class TestEmployeeResourcePut:

    def test_when_updated(self, client: FlaskClient, app: Flask, employee_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(EmployeeModel(**employee_model_data))
            sa.session.commit()

        changes = {'age': 45}
        response = client.put(f"employees/{employee_model_data.pop('full_name')}", json=employee_model_data | changes)

        assert 201 == response.status_code
        assert changes['age'] == response.json['age']

    def test_when_company_id_not_found(self, client: FlaskClient, app: Flask) -> None:
        with app.app_context():
            sa.session.add(EmployeeModel(full_name='Employee'))
            sa.session.commit()
        response = client.put('/employees/Employee', json={'company_id': 999})

        assert 400 == response.status_code
        assert b'Company id not found' in response.data

    def test_when_validation_error_occurs(self, client: FlaskClient, app: Flask) -> None:
        with app.app_context():
            sa.session.add(EmployeeModel(full_name='Employee'))
            sa.session.commit()

        response = client.put('employees/Employee', json={'company_id': 1})

        assert 400 == response.status_code
        assert b'field required' in response.data

    def test_when_employee_not_found(self, app, client: FlaskClient) -> None:
        response = client.put('employees/Employee', json={})

        assert 400 == response.status_code
        assert b'Employee not found' in response.data
