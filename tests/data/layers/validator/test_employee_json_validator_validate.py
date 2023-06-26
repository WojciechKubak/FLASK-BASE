import pytest


class TestEmployeeJsonValidatorValidate:

    def test_when_employee_data_is_not_correct(self, employee_record_test, employee_validator_obj):
        employee_record_test['first_name'] = 'First1Name'
        with pytest.raises(ValueError) as err:
            employee_validator_obj.validate(employee_record_test)
        assert 'first_name: does not match condition' == str(err.value)

    def test_when_employee_data_is_correct(self, employee_record_test, employee_validator_obj):
        assert employee_validator_obj.validate(employee_record_test) == employee_record_test
