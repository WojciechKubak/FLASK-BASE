from app.service.service.employee import EmployeeService
from app.data.model.employee import Employee
import pytest


class TestAddOrUpdate:

    @pytest.mark.parametrize('employee_obj_with_expected_id', ['10'], indirect=True)
    def test_when_adding_new_record(
            self,
            employee_service: EmployeeService,
            employee_obj_with_expected_id: Employee
    ) -> None:
        employee_service.add_or_update(employee_obj_with_expected_id)
        assert employee_obj_with_expected_id == employee_service.find_by_id(10)

    @pytest.mark.parametrize('employee_obj_with_expected_id', ['0'], indirect=True)
    def test_when_updating_existing_record(
            self,
            employee_service: EmployeeService,
            employee_obj_with_expected_id: Employee
    ) -> None:
        employee_service.add_or_update(employee_obj_with_expected_id)
        assert employee_obj_with_expected_id == employee_service.find_by_id(0)
