from app.model.user import UserModel
from werkzeug.security import generate_password_hash
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, order=True)
class UserService:

    def add_user(self, data: dict[str, Any]) -> None:
        if data['password'] != data.pop('password_repeat'):
            raise ValueError('Passwords must be the same')
        if UserModel.find_by_username(data['username']):
            raise ValueError('Username is already in use')
        if UserModel.find_by_email(data['email']):
            raise ValueError('Email is already in use')

        data['password'] = generate_password_hash(data['password'])

        user = UserModel(**data)
        user.add()

    def update_user(self, data: dict[str, Any]) -> None:
        if not (user := UserModel.find_by_username(data['username'])):
            raise ValueError('User does not exist')
        if UserModel.find_by_email(data['email']):
            raise ValueError('Email is already in use')
        if data['password'] != data['password_repeat']:
            raise ValueError('Passwords must be the same')

        user.update(data)

    def delete_user(self, username: str) -> None:
        if not (user := UserModel.find_by_username(username)):
            raise ValueError('User does not exist')
        user.delete()

    def activate_user(self, username: str) -> None:
        if user := UserModel.find_by_username(username):
            user.update({'is_active': True})

    def check_login_credentials(self, username: str, password: str) -> UserModel:
        if not (user := UserModel.find_by_username(username)):
            raise ValueError('User does not exist')
        if not user.check_password(password):
            raise ValueError('Incorrect password provided')
        if not user.is_active:
            raise ValueError('User is not activated')
        return user

    def check_user_password(self, username: str, password: str) -> None:
        user = UserModel.find_by_username(username)
        if not user.check_password(password):
            raise ValueError('Incorrect password provided')

    def check_if_user_is_active(self, username: str) -> None:
        user = UserModel.find_by_username(username)
        if not user.is_active:
            raise ValueError('User is not activated')

    def get_user_by_name(self, username: str) -> UserModel:
        if not (user := UserModel.find_by_username(username)):
            raise ValueError('User not found')
        return user
