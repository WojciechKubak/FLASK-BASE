from app.data.layers.validator import Validator
from typing import Any
import pytest


class TestValidatorValidateValue:

    def test_when_key_not_found_in_data(self, company_record_test: dict[str, Any]) -> None:
        assert Validator.validate_value(company_record_test, 'non_existing_key', lambda x: x) == 'key not found'

    def test_when_value_does_not_match_condition(self, company_record_test: dict[str, Any]) -> None:
        assert Validator.validate_value(company_record_test, 'company_name', lambda x: False) \
               == 'does not match condition'

    def test_when_value_matches_condition(self, company_record_test: dict[str, Any]) -> None:
        assert not Validator.validate_value(company_record_test, 'company_name', lambda x: True)





