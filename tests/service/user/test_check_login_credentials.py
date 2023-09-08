from app.service.user import UserService
from app.model.user import UserModel
from app.db.configuration import sa
from app.security.configuration import bcrypt
from flask import Flask
from typing import Any
import pytest


class TestUserServiceCheckLoginCredentials:
    user_service = UserService()

    @pytest.fixture(autouse=True, scope='function')
    def add_user_with_hashed_password(self, app: Flask, user_model_data: dict[str, Any]) -> None:
        with app.app_context():
            hashed_password = bcrypt.generate_password_hash(user_model_data['password'])
            sa.session.add(UserModel(**user_model_data | {'password': hashed_password}))
            sa.session.commit()

    def test_when_user_does_not_exist(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(ValueError) as err:
                self.user_service.check_login_credentials('User', '')

        assert 'User not found' == str(err.value)

    def test_when_password_is_incorrect(self, app: Flask, user_model_data: dict[str, Any]) -> None:
        with app.app_context():
            with pytest.raises(ValueError) as err:
                self.user_service.check_login_credentials(
                    user_model_data['username'],
                    f"{user_model_data['password']}1111"
                )

        assert 'Incorrect password provided' == str(err.value)

    def test_when_user_is_not_activated(self, app: Flask, user_model_data: dict[str, Any]) -> None:
        with app.app_context():
            with pytest.raises(ValueError) as err:
                self.user_service.check_login_credentials(
                    user_model_data['username'],
                    user_model_data['password']
                )

        assert 'User is not activated' == str(err.value)

    def test_when_credentials_are_correct(self, app: Flask, user_model_data: dict[str, Any]) -> None:
        with app.app_context():
            user = sa.session.query(UserModel).filter_by(username=user_model_data['username']).first()
            user.is_active = True
            sa.session.commit()

            result = self.user_service.check_login_credentials(
                user_model_data['username'],
                user_model_data['password']
            )

        assert user == result
