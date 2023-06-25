import pytest


class TestCompanyJsonValidatorValidate:

    def test_when_company_data_is_not_correct(self, company_record_test, company_validator_obj):
        company_record_test['city'] = 'Incorrect1City'
        with pytest.raises(ValueError) as err:
            company_validator_obj.validate(company_record_test)
        assert 'city: does not match condition' == str(err.value)

    def test_when_company_data_is_correct(self, company_record_test, company_validator_obj):
        assert company_validator_obj.validate(company_record_test) == company_record_test
