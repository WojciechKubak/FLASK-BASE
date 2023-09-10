from app.model.user import UserModel
from app.security.configuration import bcrypt
from app.data.validator import UserJsonValidator
from dataclasses import dataclass
from typing import Any, ClassVar
import json
import os


@dataclass
class UserService:
    """
    Service class for managing user-related operations.

    Attributes:
        USER_NOT_FOUND_ERROR_MSG (ClassVar[str]): Default error message for user not found.
    """

    USER_NOT_FOUND_ERROR_MSG: ClassVar[str] = 'User not found'

    def __post_init__(self):
        user_constraints = json.loads(os.environ.get('USER_CONSTRAINTS'))
        self._user_validator = UserJsonValidator(**user_constraints)

    def add_user(self, data: dict[str, Any]) -> UserModel:
        """
        Creates and adds a new user to the database.

        Args:
            data (dict[str, Any]): User data including 'username', 'email', and 'password'.

        Returns:
            UserModel: The created user model.

        Raises:
            ValueError: If the user with the same username or email already exists.
        """
        if UserModel.find_by_username(data['username']) or UserModel.find_by_email(data['email']):
            raise ValueError('User already exists')
        self._user_validator.validate(data)

        hashed_password = bcrypt.generate_password_hash(data.pop('password'))
        user = UserModel(**data, password=hashed_password)
        user.add()

        return user

    def add_admin(self, data: dict[str, Any]) -> UserModel:
        """
        Creates and adds a new admin user to the database.

        Args:
            data (dict[str, Any]): Admin user data including 'username', 'email', and 'password'.

        Returns:
            UserModel: The created admin user model.

        Raises:
            ValueError: If the admin user with the same username or email already exists.
        """
        if UserModel.find_by_username(data['username']) or UserModel.find_by_email(data['email']):
            raise ValueError('User already exists')
        self._user_validator.validate(data)

        hashed_password = bcrypt.generate_password_hash(data.pop('password'))
        user = UserModel(**data, password=hashed_password, is_active=True, role='Admin')
        user.add()

        return user

    def update_user(self, data: dict[str, Any]) -> UserModel:
        """
        Updates an existing user's information.

        Args:
            data (dict[str, Any]): Updated user data including 'username', 'email', and 'password'.

        Returns:
            UserModel: The updated user model.

        Raises:
            ValueError: If the user does not exist.
        """
        if not (user := UserModel.find_by_username(data['username'])):
            raise ValueError(self.USER_NOT_FOUND_ERROR_MSG)
        self._user_validator.validate(data)
        user.update(data | {'password': bcrypt.generate_password_hash(data['password'])})
        return user

    def delete_user(self, username: str) -> int:
        """
        Deletes a user with the specified username.

        Args:
            username (str): The username of the user to delete.

        Returns:
            int: The ID of the deleted user.

        Raises:
            ValueError: If the user does not exist.
        """
        if not (user := UserModel.find_by_username(username)):
            raise ValueError(self.USER_NOT_FOUND_ERROR_MSG)
        user.delete()
        return user.id

    def activate_user(self, username: str) -> UserModel:
        """
        Activates a user with the specified username.

        Args:
            username (str): The username of the user to activate.

        Returns:
            UserModel: The activated user model.

        Raises:
            ValueError: If the user does not exist or is already active.
        """
        if not (user := UserModel.find_by_username(username)):
            raise ValueError(self.USER_NOT_FOUND_ERROR_MSG)
        if user.is_active:
            raise ValueError('User is already active')
        user.update({'is_active': True})
        return user

    def check_login_credentials(self, username: str, password: str) -> UserModel:
        """
        Validates user login credentials.

        Args:
            username (str): The username of the user attempting to log in.
            password (str): The password provided by the user.

        Returns:
            UserModel: The user model if the credentials are valid.

        Raises:
            ValueError: If the user does not exist, the password is incorrect, or the user is not activated.
        """
        if not (user := UserModel.find_by_username(username)):
            raise ValueError(self.USER_NOT_FOUND_ERROR_MSG)
        if not user.check_password(password):
            raise ValueError('Incorrect password provided')
        if not user.is_active:
            raise ValueError('User is not activated')
        return user

    def get_user_by_name(self, username: str) -> UserModel:
        """
        Retrieves a user by username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            UserModel: The user model.

        Raises:
            ValueError: If the user does not exist.
        """
        if not (user := UserModel.find_by_username(username)):
            raise ValueError(self.USER_NOT_FOUND_ERROR_MSG)
        return user
