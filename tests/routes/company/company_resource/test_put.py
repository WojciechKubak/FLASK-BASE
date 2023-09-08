from app.model.company import CompanyModel
from app.db.configuration import sa
from flask.testing import FlaskClient
from flask import Flask
from typing import Any


class TestCompanyResourcePut:

    def test_when_updated(self, client: FlaskClient, app: Flask, company_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(CompanyModel(**company_model_data))
            sa.session.commit()

        changes = {'postal_code': '54321'}
        response = client.put(f"companies/{company_model_data.pop('name')}", json=company_model_data | changes)

        assert 201 == response.status_code
        assert changes['postal_code'] == response.json['postal_code']

    def test_when_validation_error_occurs(self, client: FlaskClient, app: Flask) -> None:
        with app.app_context():
            sa.session.add(CompanyModel(name='Company'))
            sa.session.commit()

        response = client.put('companies/Company', json={})

        assert 400 == response.status_code
        assert b'field required' in response.data

    def test_when_company_not_found(self, client: FlaskClient) -> None:
        response = client.put('companies/Company', json={})

        assert 400 == response.status_code
        assert b'Company not found' in response.data
