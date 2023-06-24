from app.data.organization.employee import Employee
from typing import Any
from decimal import Decimal
import pytest


class TestEmployeeFromDict:

    @pytest.mark.skip('This is not prepared to be tested.')
    def test_when_data_is_not_correct(self) -> None:
        with pytest.raises(AttributeError) as err:
            Employee.from_dict({})
        assert str(err.value).startswith('Data is not correct.')

    def test_when_data_is_correct(self, employee_record_test: dict[str, Any]) -> None:
        employee = Employee.from_dict(employee_record_test)
        assert employee.salary == Decimal('7000')
