from app.model.user import UserModel
from app.db.configuration import sa
from flask import Flask
from typing import Any


def test_if_user_model_to_dict_returns_expected_values(app: Flask, user_model_data: dict[str, Any]) -> None:
    with app.app_context():
        sa.session.add(user := UserModel(**user_model_data))
        sa.session.commit()

        expected = {
            'id': user.id,
            'username': user_model_data['username'],
            'role': 'User',
            'email': user_model_data['email'],
            'active': False
        }

        assert expected == user.to_dict()
