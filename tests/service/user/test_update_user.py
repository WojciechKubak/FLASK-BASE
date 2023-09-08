from app.service.user import UserService
from app.model.user import UserModel
from app.db.configuration import sa
from typing import Any
from flask import Flask
import pytest


class TestUpdateUser:
    user_service = UserService()

    def test_when_user_does_not_exist(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(ValueError) as err:
                self.user_service.update_user({'username': 'User'})

            assert 'User not found' == str(err.value)

    def test_when_updated_succesfully(self, app: Flask, user_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(UserModel(**user_model_data))
            sa.session.commit()

            changes = {'email': 'user@example.com'}
            result = self.user_service.update_user(user_model_data | changes)

            assert changes['email'] == result.email

    def test_when_validation_error_occurrs(self, app: Flask) -> None:
        with app.app_context():
            sa.session.add(UserModel(username='User', password='password'))
            sa.session.commit()

            with pytest.raises(ValueError) as err:
                self.user_service.update_user({'username': 'User'})

        assert 'field required' in str(err.value)
