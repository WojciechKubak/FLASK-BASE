from app.service.user import UserService
from app.model.user import UserModel
from app.db.configuration import sa
from flask import Flask
from typing import Any
import pytest


class TestUserServiceGetUserByName:
    user_service = UserService()

    def test_when_user_not_found(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(ValueError) as err:
                self.user_service.get_user_by_name('User')

        assert 'User not found' == str(err.value)

    def test_when_user_found_sucessfully(self, app: Flask, user_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(user := UserModel(**user_model_data))
            sa.session.commit()

            assert user == self.user_service.get_user_by_name(user.username)
