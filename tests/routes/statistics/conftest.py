from app.model.employee import EmployeeModel
from app.model.company import CompanyModel
from app.db.configuration import sa
from typing import Any
from flask import Flask
import pytest


@pytest.fixture(autouse=True, scope='function')
def with_record_samples(
        app: Flask,
        company_records: list[dict[str, Any]],
        employee_records: list[dict[str, Any]]
) -> None:
    with app.app_context():
        sa.session.add_all([CompanyModel(**record) for record in company_records])
        sa.session.add_all([EmployeeModel(**record) for record in employee_records])
        sa.session.commit()
