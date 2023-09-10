from app.model.employee import EmployeeModel
from app.model.company import CompanyModel
from app.data.validator import EmployeeJsonValidator
from dataclasses import dataclass
from typing import Any, ClassVar
import json
import os


@dataclass
class EmployeeService:
    """
    Service class for managing employee-related operations.

    Attributes:
        EMPLOYEE_NOT_FOUND_ERROR_MSG (ClassVar[str]): Error message for when an employee is not found.
    """

    EMPLOYEE_NOT_FOUND_ERROR_MSG: ClassVar[str] = 'Employee not found'

    def __post_init__(self):
        _employee_constraints = json.loads(os.environ.get('EMPLOYEE_CONSTRAINTS'))
        self.employee_validator = EmployeeJsonValidator(**_employee_constraints)

    def add_employee(self, data: dict[str, Any]) -> EmployeeModel:
        """
        Adds a new employee to the database.

        Args:
            data (dict[str, Any]): Employee data to be added.

        Returns:
            EmployeeModel: The newly added employee.

        Raises:
            ValueError: If the employee with the same full name already exists, or if the associated
            company is not found or if data validation fails.
        """
        if EmployeeModel.find_by_name(data['full_name']):
            raise ValueError('Employee already exists')
        if not CompanyModel.find_by_id(data['company_id']):
            raise ValueError('Company id not found')

        self.employee_validator.validate(data)
        employee = EmployeeModel(**data)
        employee.add()

        return employee

    def update_employee(self, data: dict[str, Any]) -> EmployeeModel:
        """
        Updates an existing employee in the database.

        Args:
            data (dict[str, Any]): Updated employee data.

        Returns:
            EmployeeModel: The updated employee.

        Raises:
            ValueError: If the employee is not found, if the associated company is not found
            or if data validation fails.
        """
        if not (employee := EmployeeModel.find_by_name(data['full_name'])):
            raise ValueError(EmployeeService.EMPLOYEE_NOT_FOUND_ERROR_MSG)
        if not CompanyModel.find_by_id(data['company_id']):
            raise ValueError('Company id not found')

        self.employee_validator.validate(data)
        employee.update(data)

        return employee

    def delete_employee(self, name: str) -> int:
        """
        Deletes an employee from the database by their full name.

        Args:
            name (str): The full name of the employee to be deleted.

        Returns:
            int: The ID of the deleted employee.

        Raises:
            ValueError: If the employee is not found.
        """
        if not (employee := EmployeeModel.find_by_name(name)):
            raise ValueError(EmployeeService.EMPLOYEE_NOT_FOUND_ERROR_MSG)
        employee.delete()
        return employee.id

    def get_employee_by_name(self, name: str) -> EmployeeModel:
        """
        Retrieves an employee from the database by their full name.

        Args:
            name (str): The full name of the employee to retrieve.

        Returns:
            EmployeeModel: The retrieved employee.

        Raises:
            ValueError: If the employee is not found.
        """
        if not (employee := EmployeeModel.find_by_name(name)):
            raise ValueError(EmployeeService.EMPLOYEE_NOT_FOUND_ERROR_MSG)
        return employee

    def get_all_employees(self) -> list[EmployeeModel]:
        """
        Retrieves a list of all employees in the database.

        Returns:
            list[EmployeeModel]: A list of EmployeeModel objects representing all employees.
        """
        return EmployeeModel.query.all()

    def add_or_update_many(self, data: list[dict[str, Any]]) -> list[EmployeeModel]:
        """
        Adds or updates multiple employees based on the provided data.

        Args:
            data (list[dict[str, Any]]): A list of employee data to be added or updated.

        Returns:
            list[EmployeeModel]: A list of EmployeeModel objects representing the added or updated employees.
        """
        return [self.update_employee(record) if EmployeeModel.find_by_name(record['full_name'])
                else self.add_employee(record) for record in data]
