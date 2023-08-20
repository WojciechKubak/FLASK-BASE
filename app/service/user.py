from app.model.user import UserModel
from app.data.validator import UserJsonValidator
from werkzeug.security import generate_password_hash
from dataclasses import dataclass
from typing import Any, ClassVar
import json
import os


@dataclass
class UserService:
    USER_NOT_FOUND_ERROR_MSG: ClassVar[str] = 'User not found'

    def __post_init__(self):
        _user_constraints = json.loads(os.environ.get('USER_CONSTRAINTS'))
        self.user_validator = UserJsonValidator(**_user_constraints)

    def add_user(self, data: dict[str, Any], is_admin: bool = False) -> None:
        if data['password'] != data.pop('password_repeat'):
            raise ValueError('Passwords must be the same')
        if UserModel.find_by_username(data['username']):
            raise ValueError('Username is already in use')
        if UserModel.find_by_email(data['email']):
            raise ValueError('Email is already in use')

        self.user_validator.validate(data)

        data['password'] = generate_password_hash(data['password'])
        data['role'] = 'Admin' if is_admin else 'User'
        data['is_active'] = True if is_admin else False

        user = UserModel(**data)
        user.add()

    def update_user(self, data: dict[str, Any]) -> None:
        if not (user := UserModel.find_by_username(data['username'])):
            raise ValueError(self.USER_NOT_FOUND_ERROR_MSG)
        if data['password'] != data['password_repeat']:
            raise ValueError('Passwords must be the same')

        self.user_validator.validate(data)
        data['password'] = generate_password_hash(data['password'])

        user.update(data)

    def delete_user(self, username: str) -> None:
        if not (user := UserModel.find_by_username(username)):
            raise ValueError(self.USER_NOT_FOUND_ERROR_MSG)
        user.delete()

    def activate_user(self, username: str) -> None:
        if user := UserModel.find_by_username(username):
            user.update({'is_active': True})

    def check_login_credentials(self, username: str, password: str) -> UserModel:
        if not (user := UserModel.find_by_username(username)):
            raise ValueError(self.USER_NOT_FOUND_ERROR_MSG)
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
            raise ValueError(self.USER_NOT_FOUND_ERROR_MSG)
        return user
