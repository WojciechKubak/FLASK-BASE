from app.data.layers.validator import CompanyJsonValidator
from typing import Any
import pytest


def test_when_company_data_is_not_correct(
        company_record_data: dict[str, Any],
        company_validator_obj: CompanyJsonValidator
) -> None:
    company_record_data['city'] = 'Incorrect1City'
    with pytest.raises(ValueError) as err:
        company_validator_obj.validate(company_record_data)
    assert 'city: does not match condition' == str(err.value)


def test_when_company_data_is_correct(
        company_record_data: dict[str, Any],
        company_validator_obj: CompanyJsonValidator
) -> None:
    assert company_record_data == company_validator_obj.validate(company_record_data)
