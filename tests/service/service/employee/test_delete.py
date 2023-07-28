from app.service.service.employee import EmployeeService
import pytest


class TestDelete:

    def test_when_id_is_not_correct(self, employee_service: EmployeeService) -> None:
        with pytest.raises(ValueError) as err:
            employee_service.delete(-99)
        assert 'Id must be non-negative number.' == str(err.value)

    def test_when_id_is_present_in_data(self, employee_service: EmployeeService) -> None:
        record_counter = len(employee_service.find_all())
        employee_service.delete(0)
        assert not employee_service.find_by_id(0)
        assert record_counter - 1 == len(employee_service.find_all())

    def test_when_id_is_not_present_in_data(self, employee_service: EmployeeService) -> None:
        record_counter = len(employee_service.find_all())
        employee_service.delete(999)
        assert record_counter == len(employee_service.find_all())
