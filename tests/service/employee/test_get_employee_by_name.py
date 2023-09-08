from app.service.employee import EmployeeService
from app.model.employee import EmployeeModel
from app.db.configuration import sa
from flask import Flask
from typing import Any
import pytest


class TestEmployeeServiceGetEmployeeByName:
    employee_service = EmployeeService()

    def test_when_employee_not_found(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(ValueError) as err:
                self.employee_service.get_employee_by_name('Employee')

        assert 'Employee not found' == str(err.value)

    def test_when_employee_found_sucessfully(self, app: Flask, employee_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(employee := EmployeeModel(**employee_model_data))
            sa.session.commit()

            assert employee == self.employee_service.get_employee_by_name(employee_model_data['full_name'])
