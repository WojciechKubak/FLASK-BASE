from app.model.company import CompanyModel
from app.db.configuration import sa
from flask.testing import FlaskClient
from flask import Flask
from typing import Any


class TestCompanyResourcePost:

    def test_when_added(self, client: FlaskClient, app: Flask, company_model_data: dict[str, Any]) -> None:
        response = client.post(f"companies/{company_model_data.pop('name')}", json=company_model_data)

        assert 201 == response.status_code

        with app.app_context():
            assert sa.session.query(CompanyModel).first().to_dict() == response.json

    def test_when_company_exists(self, client: FlaskClient, app: Flask, company_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(CompanyModel(**company_model_data))
            sa.session.commit()

        response = client.post(f"companies/{company_model_data['name']}", json=company_model_data)

        assert 400 == response.status_code
        assert b'Company already exists' in response.data

    def test_when_validation_error_occurs(self, client: FlaskClient) -> None:
        response = client.post('companies/Company', json={})

        assert 400 == response.status_code
        assert b'field required' in response.data
