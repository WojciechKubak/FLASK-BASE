from app.data.layers.validator import EmployeeJsonValidator
from typing import Any
import pytest


class TestValidate:

    def test_when_employee_data_is_not_correct(
            self,
            employee_record_data: dict[str, Any],
            employee_validator_obj: EmployeeJsonValidator
    ) -> None:
        employee_record_data['first_name'] = 'First1Name'
        with pytest.raises(ValueError) as err:
            employee_validator_obj.validate(employee_record_data)
        assert str(err.value).endswith('does not match condition')

    def test_when_employee_data_is_correct(
            self,
            employee_record_data: dict[str, Any],
            employee_validator_obj: EmployeeJsonValidator
    ) -> None:
        assert employee_record_data == employee_validator_obj.validate(employee_record_data)
