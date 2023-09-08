from app.data.validator import Validator
import pytest


class TestMatchIfStringContainsNonNegativeNumber:

    @pytest.mark.parametrize('text,expected_type', [('123.2', int), ('-12', int), ('abc', int)])
    def test_when_text_does_not_match_expected_type_int(self, text: str, expected_type: type) -> None:
        assert not Validator.match_if_string_contains_non_negative_number(text, expected_type)

    @pytest.mark.parametrize('text,expected_type', [('0', int), ('1000', int)])
    def test_when_text_matches_expected_type_int(self, text: str, expected_type: type) -> None:
        assert Validator.match_if_string_contains_non_negative_number(text, expected_type)

    @pytest.mark.parametrize('text,expected_type', [('-12.3', float), ('def', float), ('-12', float)])
    def test_when_text_does_not_match_expected_type_float(self, text: str, expected_type: type) -> None:
        assert not Validator.match_if_string_contains_non_negative_number(text, expected_type)

    @pytest.mark.parametrize('text,expected_type', [('12', float), ('0', float), ('2.32', float)])
    def test_when_text_matches_expected_type_float(self, text: str, expected_type: type) -> None:
        assert Validator.match_if_string_contains_non_negative_number(text, expected_type)
