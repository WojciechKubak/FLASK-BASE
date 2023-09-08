from app.service.company import CompanyService
from app.model.company import CompanyModel
from app.db.configuration import sa
from flask import Flask
from typing import Any
import pytest


class TestCompanyServiceDeleteCompany:
    company_service = CompanyService()

    def test_when_company_does_not_exist(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(ValueError) as err:
                self.company_service.delete_company('Company')

        assert 'Company not found' == str(err.value)

    def test_when_deleted_sucessfully(self, app: Flask, company_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(CompanyModel(**company_model_data))
            sa.session.commit()

            self.company_service.delete_company(company_model_data['name'])

            assert not sa.session.query(CompanyModel).filter_by(name=company_model_data['name']).first()
