from app.service.employee import EmployeeService
from app.model.employee import EmployeeModel
from app.db.configuration import sa
from typing import Any
from flask import Flask
import pytest


class TestEmployeeServiceAddEmployee:
    employee_service = EmployeeService()

    def test_when_employee_already_exists(self, app: Flask, employee_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(EmployeeModel(**employee_model_data))
            sa.session.commit()

            with pytest.raises(ValueError) as err:
                self.employee_service.add_employee(employee_model_data)

        assert 'Employee already exists' == str(err.value)

    def test_when_employee_added_successfully(self, app: Flask, employee_model_data: dict[str, Any]) -> None:
        with app.app_context():
            result = self.employee_service.add_employee(employee_model_data)

            assert sa.session.query(EmployeeModel).filter_by(full_name=result.full_name).first() == result

    def test_when_validation_error_occurs(self, app: Flask, employee_model_data: dict[str, Any]) -> None:
        with app.app_context():
            with pytest.raises(ValueError) as err:
                self.employee_service.add_employee(employee_model_data | {'department': '1234'})

        assert str(err.value).endswith('does not match condition')
