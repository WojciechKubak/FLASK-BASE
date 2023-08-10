from app.db.configuration import sa
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Any, Self
from dataclasses import InitVar
from datetime import datetime
from sqlalchemy import func


class UserModel(sa.Model):

    __tablename__ = 'users'
    __allow_unmapped__ = True

    # https://docs.sqlalchemy.org/en/20/orm/dataclasses.html
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str]
    role: Mapped[str] = mapped_column(default='User')
    password: InitVar[str]
    password_hash: Mapped[str]
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.utc_timestamp(), default=None)

    def __post_init__(self, password: str):
        self.password_hash = generate_password_hash(password)

    def to_dict(self) -> dict[str, Any]:
        return {
            'username': self.username,
            'role': self.username,
            'email': self.email,
            'active': self.is_active
        }

    def add_or_update(self) -> None:
        sa.session.add(self)
        sa.session.commit()

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def delete(self) -> None:
        sa.session.delete(self)
        sa.session.commit()

    @classmethod
    def find_by_username(cls: Self, username: str) -> Self:
        return UserModel.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls: Self, email: str) -> Self:
        return UserModel.query.filter_by(email=email).first()
