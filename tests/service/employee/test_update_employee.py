from app.service.employee import EmployeeService
from app.model.employee import EmployeeModel
from app.db.configuration import sa
from typing import Any
from flask import Flask
import pytest


class TestEmployeeServiceUpdateEmployee:
    employee_service = EmployeeService()

    def test_when_employee_does_not_exist(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(ValueError) as err:
                self.employee_service.update_employee({'full_name': 'Employee'})

        assert 'Employee not found' == str(err.value)

    def test_when_updated_succesfully(self, app: Flask, employee_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(EmployeeModel(**employee_model_data))
            sa.session.commit()

            expected = sa.session.query(EmployeeModel).filter_by(full_name=employee_model_data['full_name']).first()

            assert expected == self.employee_service.update_employee(employee_model_data | {'postal_code': '54321'})

    def test_when_validation_error_occurs(self, app: Flask, employee_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(EmployeeModel(**employee_model_data))
            sa.session.commit()

            with pytest.raises(ValueError) as err:
                self.employee_service.update_employee(employee_model_data | {'salary': -39000})

        assert str(err.value).endswith('does not match condition')
