from app.service.repository.repository import EmployeeRepository
from app.data.model.employee import Employee
from typing import Any
import pytest


@pytest.fixture
def employee_obj(request: Any, employee_record_data: dict[str, Any]) -> Employee:
    employee_record_data['id'] = request.param
    return Employee.from_dict(employee_record_data)


@pytest.mark.parametrize('employee_obj', ['10', '2'], indirect=True)
def test_when_adding_new_record(
        employee_repository: EmployeeRepository,
        employee_obj: Employee
) -> None:
    employee_repository.add_or_update(employee_obj)
    assert employee_obj in employee_repository.employees
