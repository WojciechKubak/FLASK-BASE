from app.model.company import CompanyModel
from app.db.configuration import sa
from flask import Flask
from typing import Any


class TestCompanyModelCrudMethods:

    def test_add(self, app: Flask, company_model_data: dict[str, Any]) -> None:
        with app.app_context():
            company = CompanyModel(**company_model_data)
            company.add()

            assert sa.session.query(CompanyModel).filter_by(id=company.id).first() == company

    def test_delete(self, app: Flask) -> None:
        with app.app_context():
            sa.session.add(company := CompanyModel(name='Company'))
            sa.session.commit()

            company.delete()

            assert not sa.session.query(CompanyModel).filter_by(id=company.id).first()

    def test_update(self, app: Flask) -> None:
        with app.app_context():
            sa.session.add(company := CompanyModel(name='Company'))
            sa.session.commit()

            changes = {'postal_code': '54321'}
            company.update(changes)

            assert changes['postal_code'] == company.postal_code

    def test_find_by_id(self, app: Flask) -> None:
        with app.app_context():
            sa.session.add(company := CompanyModel(name='Company'))
            sa.session.commit()

            assert company == CompanyModel.find_by_id(company.id)

    def test_find_by_name(self, app: Flask) -> None:
        with app.app_context():
            sa.session.add(company := CompanyModel(name='Company'))
            sa.session.commit()

            assert company == CompanyModel.find_by_name(company.name)
