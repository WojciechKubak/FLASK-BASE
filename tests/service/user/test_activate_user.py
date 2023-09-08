from app.service.user import UserService
from app.model.user import UserModel
from app.db.configuration import sa
from flask import Flask
import pytest


class TestUserServiceActivateUser:
    user_service = UserService()

    def test_when_user_does_not_exist(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(ValueError) as err:
                self.user_service.activate_user('User')

        assert 'User not found' == str(err.value)

    def test_when_user_is_already_active(self, app: Flask) -> None:
        with app.app_context():
            sa.session.add(UserModel(username='User', password='password', is_active=True))
            sa.session.commit()

            with pytest.raises(ValueError) as err:
                self.user_service.activate_user('User')

        assert 'User is already active' == str(err.value)

    def test_when_user_activated_succesfully(self, app: Flask) -> None:
        with app.app_context():
            sa.session.add(user := UserModel(username='User', password='password'))
            sa.session.commit()

            self.user_service.activate_user(user.username)

            assert sa.session.query(UserModel).filter_by(username=user.username).first().is_active
