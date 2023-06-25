from app.data.layers.validator import CompanyJsonValidator
from typing import Any
import pytest


class TestCompanyJsonValidatorValidate:

    def test_when_company_data_is_not_correct(
            self,
            company_record_test: dict[str, Any],
            company_validator_obj: CompanyJsonValidator
    ) -> None:
        company_record_test['city'] = 'Incorrect1City'
        with pytest.raises(ValueError) as err:
            company_validator_obj.validate(company_record_test)
        assert 'city: does not match condition' == str(err.value)

    def test_when_company_data_is_correct(
            self,
            company_record_test: dict[str, Any],
            company_validator_obj: CompanyJsonValidator
    ) -> None:
        assert company_validator_obj.validate(company_record_test) == company_record_test
