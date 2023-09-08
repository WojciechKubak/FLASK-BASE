from app.service.company import CompanyService
from app.model.company import CompanyModel
from app.db.configuration import sa
from flask import Flask
from typing import Any


def test_company_service_get_all_companies(app: Flask, company_records: list[dict[str, Any]]) -> None:
    with app.app_context():
        sa.session.add_all([CompanyModel(**data) for data in company_records])
        sa.session.commit()

        assert sa.session.query(CompanyModel).all() == CompanyService().get_all_companies()
