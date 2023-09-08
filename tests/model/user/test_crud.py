from app.model.user import UserModel
from app.db.configuration import sa
from flask import Flask
from typing import Any


class TestUserModelCrudMethods:

    def test_add(self, app: Flask, user_model_data: dict[str, Any]) -> None:
        with app.app_context():
            user = UserModel(**user_model_data)
            user.add()

            assert sa.session.query(UserModel).filter_by(id=user.id).first() == user

    def test_delete(self, app: Flask) -> None:
        with app.app_context():
            sa.session.add(user := UserModel(username='User', password='password'))
            sa.session.commit()

            user.delete()

            assert not sa.session.query(UserModel).filter_by(id=user.id).first()

    def test_update(self, app: Flask) -> None:
        with app.app_context():
            sa.session.add(user := UserModel(username='User', password='password'))
            sa.session.commit()

            changes = {'email': 'new@example.com'}
            user.update(changes)

            assert changes['email'] == user.email

    def test_find_by_username(self, app: Flask) -> None:
        with app.app_context():
            sa.session.add(user := UserModel(username='User', password='password'))
            sa.session.commit()

            assert user == UserModel.find_by_username(user.username)

    def test_find_by_email(self, app: Flask) -> None:
        with app.app_context():
            sa.session.add(user := UserModel(username='User', password='password'))
            sa.session.commit()

            assert user == UserModel.find_by_email(user.email)
