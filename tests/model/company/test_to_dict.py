from app.model.company import CompanyModel
from app.model.employee import EmployeeModel
from app.db.configuration import sa
from flask import Flask
from typing import Any


class TestCompanyModelToDict:

    def test_if_returns_expected_values(self, app: Flask, company_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(CompanyModel(**company_model_data))
            sa.session.commit()

            result = sa.session.query(CompanyModel).filter_by(name=company_model_data['name']).first().to_dict()

            assert all([v == result[k] for k, v in company_model_data.items()])

    def test_when_company_has_no_employees(self, app: Flask) -> None:
        with app.app_context():
            sa.session.add(company := CompanyModel(name='Company'))
            sa.session.commit()

            assert not sa.session.query(CompanyModel).filter_by(id=company.id).first().employees

    def test_when_company_has_employees(self, app: Flask) -> None:
        with app.app_context():
            sa.session.add(company := CompanyModel(name='Company'))
            sa.session.commit()
            sa.session.add(EmployeeModel(full_name='Employee', company_id=company.id))

            assert sa.session.query(CompanyModel).filter_by(id=company.id).first().employees
