from app.service.company import CompanyService
from app.model.company import CompanyModel
from app.db.configuration import sa
from flask import Flask
from typing import Any


class TestCompanyServiceAddOrUpdateMany:
    company_service = CompanyService()

    def test_when_adding_new_records(self, app: Flask, company_records: list[dict[str, Any]]) -> None:
        with app.app_context():
            result = self.company_service.add_or_update_many(company_records)

            assert sa.session.query(CompanyModel).all() == result

    def test_when_updating_existing_records(self, app: Flask, company_records: list[dict[str, Any]]) -> None:
        with app.app_context():
            sa.session.add_all([CompanyModel(**data) for data in company_records])

            updated = [record | {'city': 'NewCity'} for record in company_records]
            result = self.company_service.add_or_update_many(updated)

            assert sa.session.query(CompanyModel).all() == result
