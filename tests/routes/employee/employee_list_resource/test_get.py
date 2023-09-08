from flask.testing import FlaskClient
from app.db.configuration import sa
from app.model.employee import EmployeeModel
from flask import Flask
from typing import Any
import json


def test_employee_list_resource_get(client: FlaskClient, app: Flask, employee_records: list[dict[str, Any]]) -> None:
    with app.app_context():
        sa.session.add_all(EmployeeModel(**record) for record in employee_records)
        sa.session.commit()

    response = client.get('/employees')

    assert 200 == response.status_code
    assert len(employee_records) == len(response.json.get('employees'))
