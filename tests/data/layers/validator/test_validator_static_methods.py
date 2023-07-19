from app.data.layers.validator import Validator, CompanyJsonValidator
from typing import Any
import pytest


class TestCompanyJsonValidatorValidate:

    def test_when_company_data_is_not_correct(
            self,
            company_record_data: dict[str, Any],
            company_validator_obj: CompanyJsonValidator
    ) -> None:
        company_record_data['city'] = 'Incorrect1City'
        with pytest.raises(ValueError) as err:
            company_validator_obj.validate(company_record_data)
        assert 'city: does not match condition' == str(err.value)

    def test_when_company_data_is_correct(
            self,
            company_record_data: dict[str, Any],
            company_validator_obj: CompanyJsonValidator
    ) -> None:
        assert company_validator_obj.validate(company_record_data) == company_record_data


class TestValidatorMatchRegex:

    def test_when_regex_is_matched(self) -> None:
        assert Validator.match_regex('1234', r'^\d+$')

    def test_when_regex_is_not_matched(self) -> None:
        assert not Validator.match_regex('abcdef1', r'^[a-z]+$')


class TestValidatorMatchIfStringContainsNonNegativeNumber:

    @pytest.mark.parametrize('text,expected_type', [('123.2', int), ('-12', int), ('abcdef', int)])
    def test_when_text_does_not_match_expected_type_int(self, text: str, expected_type: type) -> None:
        assert not Validator.match_if_string_contains_non_negative_number(text, expected_type)

    @pytest.mark.parametrize('text,expected_type', [('0', int), ('1000', int)])
    def test_when_text_matches_expected_type_int(self, text: str, expected_type: type) -> None:
        assert Validator.match_if_string_contains_non_negative_number(text, expected_type)

    @pytest.mark.parametrize('text,expected_type', [('-12.3', float), ('abcdef', float), ('-12', float)])
    def test_when_text_does_not_match_expected_type_float(self, text: str, expected_type: type) -> None:
        assert not Validator.match_if_string_contains_non_negative_number(text, expected_type)

    @pytest.mark.parametrize('text,expected_type', [('12', float), ('0', float), ('2.32', float)])
    def test_when_text_matches_expected_type_float(self, text: str, expected_type: type) -> None:
        assert Validator.match_if_string_contains_non_negative_number(text, expected_type)
