from app.service.employee import EmployeeService
from app.model.employee import EmployeeModel
from app.db.configuration import sa
from flask import Flask
from typing import Any


def test_employee_service_get_all_companies(app: Flask, employee_records: list[dict[str, Any]]) -> None:
    with app.app_context():
        sa.session.add_all([EmployeeModel(**data) for data in employee_records])
        sa.session.commit()

        assert sa.session.query(EmployeeModel).all() == EmployeeService().get_all_employees()
