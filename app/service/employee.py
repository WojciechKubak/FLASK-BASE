from app.model.employee import EmployeeModel
from app.model.company import CompanyModel
from app.data.validator import EmployeeJsonValidator
from dataclasses import dataclass
from typing import Any, ClassVar
import json
import os


@dataclass
class EmployeeService:
    EMPLOYEE_NOT_FOUND_ERROR_MSG: ClassVar[str] = 'Employee not found'

    def __post_init__(self):
        _employee_constraints = json.loads(os.environ.get('EMPLOYEE_CONSTRAINTS'))
        self.employee_validator = EmployeeJsonValidator(**_employee_constraints)

    def add_employee(self, data: dict[str, Any]) -> None:
        if EmployeeModel.find_by_name(data['full_name']):
            raise ValueError('Employee already exists')
        if not CompanyModel.find_by_id(data['company_id']):
            raise ValueError('Company id not found')

        self.employee_validator.validate(data)
        employee = EmployeeModel(**data)
        employee.add()

    def update_employee(self, data: dict[str, Any]) -> None:
        if not CompanyModel.find_by_id(data['company_id']):
            raise ValueError('Company id not found')
        if not (employee := EmployeeModel.find_by_name(data['full_name'])):
            raise ValueError(EmployeeService.EMPLOYEE_NOT_FOUND_ERROR_MSG)

        self.employee_validator.validate(data)
        employee.update(data)

    def delete_employee(self, name: str) -> None:
        if not (employee := EmployeeModel.find_by_name(name)):
            raise ValueError(EmployeeService.EMPLOYEE_NOT_FOUND_ERROR_MSG)
        employee.delete()

    def get_employee_by_name(self, name: str) -> EmployeeModel:
        if not (employee := EmployeeModel.find_by_name(name)):
            raise ValueError(EmployeeService.EMPLOYEE_NOT_FOUND_ERROR_MSG)
        return employee

    def get_all_employees(self) -> list[EmployeeModel]:
        return EmployeeModel.query.all()

    def add_or_update_many(self, data: list[dict[str, Any]]) -> None:
        for record in data:
            if CompanyModel.find_by_id(record['company_id']):
                self.update_employee(record)
            else:
                self.add_employee(record)
