from app.data.validator import EmployeeJsonValidator
from typing import Any
import pytest
import json
import os


@pytest.fixture
def employee_validator_obj() -> EmployeeJsonValidator:
    constraints = json.loads(os.environ.get('EMPLOYEE_CONSTRAINTS'))
    return EmployeeJsonValidator(**constraints)


class TestValidate:

    def test_when_employee_data_does_not_match_condition(
            self,
            employee_json_data: dict[str, Any],
            employee_validator_obj: EmployeeJsonValidator
    ) -> None:
        employee_json_data['full_name'] = 'Full1Name'
        with pytest.raises(ValueError) as err:
            employee_validator_obj.validate(employee_json_data)
        assert str(err.value).endswith('does not match condition')

    def test_when_employee_data_field_is_missing(
            self,
            employee_json_data: dict[str, Any],
            employee_validator_obj: EmployeeJsonValidator
    ) -> None:
        del employee_json_data['age']
        with pytest.raises(ValueError) as err:
            employee_validator_obj.validate(employee_json_data)
        assert str(err.value).endswith('field required')

    def test_when_employee_data_is_correct(
            self,
            employee_json_data: dict[str, Any],
            employee_validator_obj: EmployeeJsonValidator
    ) -> None:
        assert employee_json_data == employee_validator_obj.validate(employee_json_data)
