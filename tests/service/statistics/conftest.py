from app.model.employee import EmployeeModel
from app.model.company import CompanyModel
from app.db.configuration import sa
from flask import Flask
from typing import Any
import pytest


@pytest.fixture(autouse=True, scope='function')
def with_record_samples(
        app: Flask,
        company_records: list[dict[str, Any]],
        employee_records: list[dict[str, Any]]
) -> None:
    with app.app_context():
        sa.session.add_all([
            *[CompanyModel(**record) for record in company_records],
            *[EmployeeModel(**record) for record in employee_records],
        ])
        sa.session.commit()
