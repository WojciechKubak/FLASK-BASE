from flask.testing import FlaskClient
from app.model.employee import EmployeeModel
from app.db.configuration import sa
from flask import Flask
from typing import Any


class TestEmployeeListResourcePost:

    def test_when_added(self, client: FlaskClient, app: Flask, employee_model_data: dict[str, Any]) -> None:
        response = client.post('/employees', json={'employees': [employee_model_data]})

        assert 201 == response.status_code

        with app.app_context():
            assert sa.session.query(EmployeeModel).filter_by(full_name=employee_model_data['full_name'])

    def test_when_updated(self, client: FlaskClient, app: Flask, employee_records: list[dict[str, Any]]) -> None:
        response = client.post('/employees', json={'employees': employee_records})

        assert 201 == response.status_code

        with app.app_context():
            assert len(employee_records) == len(sa.session.query(EmployeeModel).all())

    def test_when_company_id_not_found(self, client: FlaskClient, app: Flask) -> None:
        response = client.post('/employees', json={'employees': [{'full_name': 'Employee', 'company_id': 999}]})

        assert 400 == response.status_code
        assert b'Company id not found' in response.data

    def test_when_validation_error_occurs(self, client: Flask) -> None:
        response = client.post('/employees', json={'employees': [{'full_name': 'Employee', 'company_id': 1}]})

        assert 400 == response.status_code
        assert b'field required' in response.data
