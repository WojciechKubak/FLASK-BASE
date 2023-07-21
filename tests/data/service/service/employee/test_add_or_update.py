from app.service.service.employee import EmployeeService
from app.data.model.employee import Employee
from typing import Any
import pytest


@pytest.fixture
def employee_obj(request: Any, employee_record_data: dict[str, Any]) -> Employee:
    employee_record_data['id'] = request.param
    return Employee.from_dict(employee_record_data)


class TestAddOrUpdate:

    @pytest.mark.parametrize('employee_obj', ['10'], indirect=True)
    def test_when_adding_new_record(
            self,
            employee_service: EmployeeService,
            employee_obj: Employee
    ) -> None:
        employee_service.add_or_update(employee_obj)
        assert 5 == len(employee_service.find_all())
        assert employee_obj == employee_service.find_by_id(10)

    @pytest.mark.parametrize('employee_obj', ['0'], indirect=True)
    def test_when_updating_existing_record(
            self,
            employee_service: EmployeeService,
            employee_obj: Employee
    ) -> None:
        employee_service.add_or_update(employee_obj)
        assert 4 == len(employee_service.find_all())
        assert employee_obj == employee_service.find_by_id(0)
