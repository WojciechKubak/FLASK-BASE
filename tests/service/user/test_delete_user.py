from app.service.user import UserService
from app.model.user import UserModel
from app.db.configuration import sa
from flask import Flask
from typing import Any
import pytest


class TestUserServiceDeleteUser:
    user_service = UserService()

    def test_when_user_does_not_exist(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(ValueError) as err:
                self.user_service.delete_user('User')

        assert 'User not found' == str(err.value)

    def test_when_deleted_sucessfully(self, app: Flask, user_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(user := UserModel(**user_model_data))
            sa.session.commit()

            self.user_service.delete_user(user.username)

            assert not sa.session.query(UserModel).filter_by(username=user.username).first()
