from app.data.layers.validator import EmployeeJsonValidator
from typing import Any
import pytest


def test_when_employee_data_is_not_correct(
        employee_record_test: dict[str, Any],
        employee_validator_obj: EmployeeJsonValidator
) -> None:
    employee_record_test['first_name'] = 'First1Name'
    with pytest.raises(ValueError) as err:
        employee_validator_obj.validate(employee_record_test)
    assert 'first_name: does not match condition' == str(err.value)


def test_when_employee_data_is_correct(
        employee_record_test: dict[str, Any],
        employee_validator_obj: EmployeeJsonValidator
) -> None:
    assert employee_record_test == employee_validator_obj.validate(employee_record_test)
