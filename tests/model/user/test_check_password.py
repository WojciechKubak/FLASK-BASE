from app.model.user import UserModel
from app.db.configuration import sa
from app.security.configuration import bcrypt
from flask import Flask
from typing import Any
import pytest


class TestUserModelCheckPassword:
    password = 'password'

    @pytest.fixture
    def user_with_password_hashed(self, user_model_data: dict[str, Any]) -> dict[str, Any]:
        user_model_data['password'] = bcrypt.generate_password_hash(self.password)
        return user_model_data

    def test_when_password_is_correct(self, app: Flask, user_with_password_hashed: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(user := UserModel(**user_with_password_hashed))
            sa.session.commit()

            assert user.check_password(self.password)

    def test_when_password_is_incorrect(self, app: Flask, user_with_password_hashed: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(user := UserModel(**user_with_password_hashed))
            sa.session.commit()

            assert not user.check_password(f'{self.password}111')
