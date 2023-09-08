from app.service.employee import EmployeeService
from app.model.employee import EmployeeModel
from app.db.configuration import sa
from flask import Flask
from typing import Any
import pytest


class TestEmployeeServiceDeleteEmployee:
    employee_service = EmployeeService()

    def test_when_employee_does_not_exist(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(ValueError) as err:
                self.employee_service.delete_employee('Employee')

        assert 'Employee not found' == str(err.value)

    def test_when_deleted_sucessfully(self, app: Flask, employee_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(EmployeeModel(**employee_model_data))
            sa.session.commit()

            self.employee_service.delete_employee(employee_model_data['full_name'])

            assert not sa.session.query(EmployeeModel).filter_by(full_name=employee_model_data['full_name']).first()
