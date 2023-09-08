from app.service.employee import EmployeeService
from app.model.employee import EmployeeModel
from app.db.configuration import sa
from typing import Any
from flask import Flask


class TestEmployeeServiceAddOrUpdateMany:
    employee_service = EmployeeService()

    def test_when_adding_new_records(self, app: Flask, employee_records: list[dict[str, Any]]) -> None:
        with app.app_context():
            result = self.employee_service.add_or_update_many(employee_records)

            assert sa.session.query(EmployeeModel).all() == result

    def test_when_updating_existing_records(self, app: Flask, employee_records: list[dict[str, Any]]) -> None:
        with app.app_context():
            sa.session.add_all([EmployeeModel(**record) for record in employee_records])
            sa.session.commit()

            updated = [record | {'salary': 77000} for record in employee_records]
            result = self.employee_service.add_or_update_many(updated)

            assert sa.session.query(EmployeeModel).all() == result
