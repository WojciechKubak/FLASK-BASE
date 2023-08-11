from app.model.employee import EmployeeModel
from dataclasses import dataclass
from typing import Any, ClassVar


@dataclass(frozen=True, order=True)
class EmployeeService:
    EMPLOYEE_NOT_FOUND_ERROR_MSG: ClassVar[str] = 'Employee not found'

    def add_employee(self, data: dict[str, Any]) -> None:
        if EmployeeModel.find_by_name(data['full_name']):
            raise ValueError('Employee already exists')
        employee = EmployeeModel(**data)
        employee.add()

    def update_employee(self, data: dict[str, Any]) -> None:
        if not (employee := EmployeeModel.find_by_name(data['full_name'])):
            raise ValueError(EmployeeService.EMPLOYEE_NOT_FOUND_ERROR_MSG)
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
            if result := EmployeeModel.find_by_name(record['full_name']):
                result.update(record)
            else:
                EmployeeModel(**record).add()
