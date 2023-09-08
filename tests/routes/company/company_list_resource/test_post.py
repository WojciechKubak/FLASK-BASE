from flask.testing import FlaskClient
from app.model.company import CompanyModel
from app.db.configuration import sa
from flask import Flask
from typing import Any


class TestCompanyListResourcePost:

    def test_when_added(self, client: FlaskClient, app: Flask, company_model_data: dict[str, Any]) -> None:
        response = client.post('/companies', json={'companies': [company_model_data]})

        assert 201 == response.status_code

        with app.app_context():
            assert sa.session.query(CompanyModel).filter_by(name=company_model_data['name'])

    def test_when_updated(self, client: FlaskClient, app: Flask, company_records: list[dict[str, Any]]) -> None:
        response = client.post('/companies', json={'companies': company_records})

        assert 201 == response.status_code

        with app.app_context():
            assert len(company_records) == len(sa.session.query(CompanyModel).all())

    def test_when_validation_error_occurs(self, client: Flask) -> None:
        response = client.post('/companies', json={'companies': [{'name': 'Company'}]})

        assert 400 == response.status_code
        assert b'field required' in response.data
