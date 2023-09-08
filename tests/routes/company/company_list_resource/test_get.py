from flask.testing import FlaskClient
from app.db.configuration import sa
from app.model.company import CompanyModel
from flask import Flask
from typing import Any


def test_company_list_resource_get(client: FlaskClient, app: Flask, company_records: list[dict[str, Any]]) -> None:
    with app.app_context():
        sa.session.add_all(CompanyModel(**record) for record in company_records)
        sa.session.commit()

    response = client.get('/companies')

    assert response.status_code == 200
    assert len(company_records) == len(response.json.get('companies'))
