from app.db.configuration import sa
from werkzeug.security import check_password_hash
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime
from typing import Any, Self


class UserModel(sa.Model):

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
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'email': self.email,
            'active': self.is_active
        }

    def add(self) -> None:
        sa.session.add(self)
        sa.session.commit()

    def update(self, data: dict[str, Any]) -> None:
        for field_name, value in data.items():
            if hasattr(self, field_name):
                setattr(self, field_name, value)
        sa.session.commit()

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def delete(self) -> None:
        sa.session.delete(self)
        sa.session.commit()

    @classmethod
    def find_by_username(cls: Self, username: str) -> Self:
        return UserModel.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls: Self, email: str) -> Self:
        return UserModel.query.filter_by(email=email).first()
