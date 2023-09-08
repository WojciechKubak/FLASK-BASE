from app.model.company import CompanyModel
from app.db.configuration import sa
from flask import Flask
from typing import Any
import pytest


@pytest.fixture(autouse=True, scope='function')
def add_companies(app: Flask, company_records: list[dict[str, Any]]) -> None:
    with app.app_context():
        sa.session.add_all(CompanyModel(**record) for record in company_records)
        sa.session.commit()
