from app.data.validator import CompanyJsonValidator
from typing import Any
import pytest
import json
import os


@pytest.fixture
def company_validator_obj() -> CompanyJsonValidator:
    constraints = json.loads(os.environ.get('COMPANY_CONSTRAINTS'))
    return CompanyJsonValidator(**constraints)


class TestValidate:

    def test_when_company_data_does_not_match_condition(
            self,
            company_json_data: dict[str, Any],
            company_validator_obj: CompanyJsonValidator
    ) -> None:
        company_json_data['city'] = 'Incorrect1City'
        with pytest.raises(ValueError) as err:
            company_validator_obj.validate(company_json_data)
        assert str(err.value).endswith('does not match condition')

    def test_when_company_data_field_is_missing(
            self,
            company_json_data: dict[str, Any],
            company_validator_obj: CompanyJsonValidator
    ) -> None:
        del company_json_data['city']
        with pytest.raises(ValueError) as err:
            company_validator_obj.validate(company_json_data)
        assert str(err.value).endswith('field required')

    def test_when_company_data_is_correct(
            self,
            company_json_data: dict[str, Any],
            company_validator_obj: CompanyJsonValidator
    ) -> None:
        assert company_json_data == company_validator_obj.validate(company_json_data)
