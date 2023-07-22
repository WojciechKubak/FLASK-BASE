from app.data.layers.validator import Validator
import pytest


@pytest.mark.parametrize(
    'test_input,expected', [
        (('', r'^[A-Z]+$'), False),
        (('1234', r'^\d+$'), True),
        (('abc1', r'^[a-z]+$'), False),
        (('Example company', r'^[a-zA-Z0-9 .]+$'), True)
    ]
)
def test_match_regex(test_input: tuple[str, str], expected: bool) -> None:
    assert expected is Validator.match_regex(*test_input)
