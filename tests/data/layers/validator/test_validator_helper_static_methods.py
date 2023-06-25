from app.data.layers.validator import Validator
import pytest


class TestValidatorMatchRegex:

    def test_when_regex_is_matched(self):
        assert Validator.match_regex('1234', r'^\d+$')

    def test_when_regex_is_not_matched(self):
        assert Validator.match_regex('abcdef', r'^[a-z]+$')


class TestValidatorMatchIfStringContainsNonNegativeNumber:

    @pytest.mark.parametrize('text,expected_type', [('123.2', int), ('-12', int), ('abcdef', int)])
    def test_when_text_does_not_match_expected_type_int(self, text, expected_type):
        assert not Validator.match_if_string_contains_non_negative_number(text, expected_type)

    @pytest.mark.parametrize('text,expected_type', [('0', int), ('1000', int)])
    def test_when_text_matches_expected_type_int(self, text, expected_type):
        assert Validator.match_if_string_contains_non_negative_number(text, expected_type)

    @pytest.mark.parametrize('text,expected_type', [('-12.3', float), ('abcdef', float), ('-12', float)])
    def test_when_text_does_not_match_expected_type_float(self, text, expected_type):
        assert not Validator.match_if_string_contains_non_negative_number(text, expected_type)

    @pytest.mark.parametrize('text,expected_type', [('12', float), ('0', float), ('2.32', float)])
    def test_when_text_matches_expected_type_float(self, text, expected_type):
        assert Validator.match_if_string_contains_non_negative_number(text, expected_type)
