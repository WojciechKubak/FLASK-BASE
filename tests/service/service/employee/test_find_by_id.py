from app.service.service.employee import EmployeeService
import pytest


class TestFindById:

    def test_when_employee_id_is_correct(self, employee_service: EmployeeService) -> None:
        assert employee_service.find_by_id(0)
        assert not employee_service.find_by_id(99)

    def test_when_employee_id_is_not_correct(self, employee_service: EmployeeService) -> None:
        with pytest.raises(ValueError) as err:
            employee_service.find_by_id(-3)
        assert 'Id must be non-negative number.' == str(err.value)
