from app.model.company import CompanyModel
from app.db.configuration import sa
from flask import Flask
import pytest


@pytest.fixture(autouse=True, scope='function')
def add_company(app: Flask) -> None:
    with app.app_context():
        sa.session.add(CompanyModel(name='Company'))
        sa.session.commit()
