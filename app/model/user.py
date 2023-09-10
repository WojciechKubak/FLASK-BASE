from app.security.configuration import bcrypt
from app.db.configuration import sa

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime
from typing import Any, Self


class UserModel(sa.Model):
    """
    SQLAlchemy model representing a user.

    Attributes:
        id (Mapped[int]): Primary key for the user.
        username (Mapped[str]): Username of the user.
        email (Mapped[str]): Email address of the user.
        password (Mapped[str]): Hashed password of the user.
        role (Mapped[str]): Role of the user (default is 'User').
        is_active (Mapped[bool]): Indicates whether the user account is active (default is False).

        created_at (Mapped[datetime]): Timestamp of when the user account was created.
        updated_at (Mapped[datetime]): Timestamp of when the user account was last updated.
    """

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(sa.Integer(), primary_key=True)

    username: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    email: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    password: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    role: Mapped[str] = mapped_column(sa.String(255), default='User')
    is_active: Mapped[bool] = mapped_column(sa.Boolean(), default=False)

    created_at: Mapped[datetime] = mapped_column(insert_default=func.utc_timestamp())
    updated_at: Mapped[datetime] = mapped_column(default=func.utc_timestamp(), onupdate=func.utc_timestamp())

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the user object to a dictionary.

        Returns:
            dict[str, Any]: A dictionary representation of the user.
        """
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'email': self.email,
            'active': self.is_active
        }

    def add(self) -> None:
        """
        Add the user to the database session and commit the transaction.

        Returns:
            None
        """
        sa.session.add(self)
        sa.session.commit()

    def update(self, data: dict[str, Any]) -> None:
        """
        Update the user's fields with the provided data and commit the transaction.

        Args:
            data (dict[str, Any]): The data to update the user with.

        Returns:
            None
        """
        for field_name, value in data.items():
            if hasattr(self, field_name):
                setattr(self, field_name, value)
        sa.session.commit()

    def check_password(self, password: str) -> bool:
        """
        Check if the provided password matches the user's hashed password.

        Args:
            password (str): The password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return bcrypt.check_password_hash(self.password, password)

    def delete(self) -> None:
        """
        Delete the user from the database session and commit the transaction.

        Returns:
            None
        """
        sa.session.delete(self)
        sa.session.commit()

    @classmethod
    def find_by_username(cls: Self, username: str) -> Self:
        """
        Find a user by their username.

        Args:
            username (str): The username of the user to find.

        Returns:
            Self: The found user object or None if not found.
        """
        return UserModel.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls: Self, email: str) -> Self:
        """
        Find a user by their email address.

        Args:
            email (str): The email address of the user to find.

        Returns:
            Self: The found user object or None if not found.
        """
        return UserModel.query.filter_by(email=email).first()
