from app.model.company import CompanyModel
from app.db.configuration import sa
from flask.testing import FlaskClient
from flask import Flask
from typing import Any


class TestCompanyResourceGet:

    def test_when_company_exists(self, client: FlaskClient, app: Flask, company_model_data: dict[str, Any]) -> None:
        with app.app_context():
            company = CompanyModel(**company_model_data)
            sa.session.add(company)

            response = client.get(f"/companies/{company_model_data['name']}")

            assert 200 == response.status_code
            assert company.to_dict() == response.json

    def test_when_company_does_not_exists(self, client: FlaskClient, app: Flask) -> None:
        response = client.get('/companies/Company')

        assert 400 == response.status_code
        assert b'Company not found' in response.data
