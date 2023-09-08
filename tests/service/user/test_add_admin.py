from app.service.user import UserService
from app.model.user import UserModel
from app.db.configuration import sa
from typing import Any
from flask import Flask
import pytest


class TestUserServiceAddAdmin:
    user_service = UserService()

    def test_when_user_already_exists(self, app: Flask) -> None:
        with app.app_context():
            sa.session.add(user := UserModel(username='Admin', password='password'))
            sa.session.commit()

            with pytest.raises(ValueError) as err:
                self.user_service.add_admin({'username': user.username})

            assert 'User already exists' == str(err.value)

    def test_when_user_added_successfully(self, app: Flask, user_model_data: dict[str, Any]) -> None:
        with app.app_context():
            result = self.user_service.add_admin(user_model_data)

            assert sa.session.query(UserModel).filter_by(username=user_model_data['username']).first() == result
            assert result.is_active
            assert 'Admin' == result.role

    def test_when_validation_error_occurs(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(ValueError) as err:
                self.user_service.add_admin({'username': 'Admin', 'email': ''})

            assert str(err.value).endswith('field required')
