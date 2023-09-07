from app.model.user import UserModel
from app.security.configuration import bcrypt
from app.data.validator import UserJsonValidator
from dataclasses import dataclass
from typing import Any, ClassVar
import json
import os


@dataclass
class UserService:
    USER_NOT_FOUND_ERROR_MSG: ClassVar[str] = 'User not found'

    def __post_init__(self):
        user_constraints = json.loads(os.environ.get('USER_CONSTRAINTS'))
        self._user_validator = UserJsonValidator(**user_constraints)

    def add_user(self, data: dict[str, Any]) -> UserModel:
        if UserModel.find_by_username(data['username']) or UserModel.find_by_email(data['email']):
            raise ValueError('User already exists')
        self._user_validator.validate(data)

        hashed_password = bcrypt.generate_password_hash(data.pop('password'))
        user = UserModel(**data, password=hashed_password)
        user.add()

        return user

    def add_admin(self, data: dict[str, Any]) -> UserModel:
        if UserModel.find_by_username(data['username']) or UserModel.find_by_email(data['email']):
            raise ValueError('User already exists')
        self._user_validator.validate(data)

        hashed_password = bcrypt.generate_password_hash(data.pop('password'))
        user = UserModel(**data, password=hashed_password, is_active=True, role='Admin')
        user.add()

        return user

    def update_user(self, data: dict[str, Any]) -> UserModel:
        if not (user := UserModel.find_by_username(data['username'])):
            raise ValueError(self.USER_NOT_FOUND_ERROR_MSG)
        self._user_validator.validate(data)
        user.update(data | {'password': bcrypt.generate_password_hash(data['password'])})
        return user

    def delete_user(self, username: str) -> int:
        if not (user := UserModel.find_by_username(username)):
            raise ValueError(self.USER_NOT_FOUND_ERROR_MSG)
        user.delete()
        return user.id

    def activate_user(self, username: str) -> UserModel:
        if not (user := UserModel.find_by_username(username)):
            raise ValueError(self.USER_NOT_FOUND_ERROR_MSG)
        if user.is_active:
            raise ValueError('User is already active')
        user.update({'is_active': True})
        return user

    def check_login_credentials(self, username: str, password: str) -> UserModel:
        if not (user := UserModel.find_by_username(username)):
            raise ValueError(self.USER_NOT_FOUND_ERROR_MSG)
        if not user.check_password(password):
            raise ValueError('Incorrect password provided')
        if not user.is_active:
            raise ValueError('User is not activated')
        return user

    def get_user_by_name(self, username: str) -> UserModel:
        if not (user := UserModel.find_by_username(username)):
            raise ValueError(self.USER_NOT_FOUND_ERROR_MSG)
        return user
