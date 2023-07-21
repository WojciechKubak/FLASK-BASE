from app.data.layers.validator import Validator


class TestValidatorMatchRegex:

    def test_when_regex_is_matched(self) -> None:
        assert Validator.match_regex('1234', r'^\d+$')

    def test_when_regex_is_not_matched(self) -> None:
        assert not Validator.match_regex('abcdef1', r'^[a-z]+$')
