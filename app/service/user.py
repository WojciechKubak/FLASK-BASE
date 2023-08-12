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
        if user := self.get_user_by_name(username):
            user.set_as_active()

    def get_user_by_name(self, username: str) -> UserModel:
        return UserModel.find_by_username(username)
