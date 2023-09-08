from app.model.company import CompanyModel
from app.db.configuration import sa
from flask.testing import FlaskClient
from flask import Flask
from typing import Any


class TestCompanyResourceDelete:

    def test_when_deleted(self, client: FlaskClient, app: Flask, company_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(CompanyModel(**company_model_data))
            sa.session.commit()

        response = client.delete(f"/companies/{company_model_data['name']}")

        assert 200 == response.status_code
        assert b'Deleted company with id' in response.data

    def test_when_company_does_not_exist(self, client: FlaskClient) -> None:
        response = client.delete('/companies/Company')

        assert 400 == response.status_code
        assert b'Company not found' in response.data
