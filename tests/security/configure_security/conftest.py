from app.model.user import UserModel
from app.db.configuration import sa
from app.security.configuration import bcrypt
from flask import Flask
from typing import Any
import pytest


@pytest.fixture(autouse=True, scope='function')
def add_user_with_hashed_password(app: Flask, user_model_data: dict[str, Any]) -> None:
    with app.app_context():
        hashed_password = bcrypt.generate_password_hash(user_model_data['password'])
        sa.session.add(UserModel(**user_model_data | {'password': hashed_password}, is_active=True))
        sa.session.commit()
