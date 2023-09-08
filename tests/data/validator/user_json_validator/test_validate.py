from app.data.validator import UserJsonValidator
from typing import Any
import pytest
import json
import os


@pytest.fixture
def user_validator_obj() -> UserJsonValidator:
    constraints = json.loads(os.environ.get('USER_CONSTRAINTS'))
    return UserJsonValidator(**constraints)


class TestValidate:

    def test_when_user_data_does_not_match_condition(
            self,
            user_json_data: dict[str, Any],
            user_validator_obj: UserJsonValidator
    ) -> None:
        user_json_data['username'] = 'First$Name'
        with pytest.raises(ValueError) as err:
            user_validator_obj.validate(user_json_data)
        assert str(err.value).endswith('does not match condition')

    def test_when_user_data_field_is_missing(
            self,
            user_json_data: dict[str, Any],
            user_validator_obj: UserJsonValidator
    ) -> None:
        del user_json_data['username']
        with pytest.raises(ValueError) as err:
            user_validator_obj.validate(user_json_data)
        assert str(err.value).endswith('field required')

    def test_when_user_user_is_correct(
            self,
            user_json_data: dict[str, Any],
            user_validator_obj: UserJsonValidator
    ) -> None:
        assert user_json_data == user_validator_obj.validate(user_json_data)
