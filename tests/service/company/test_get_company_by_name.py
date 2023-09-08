from app.service.company import CompanyService
from app.model.company import CompanyModel
from app.db.configuration import sa
from flask import Flask
from typing import Any
import pytest


class TestCompanyServiceGetCompanyByName:
    company_service = CompanyService()

    def test_when_company_not_found(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(ValueError) as err:
                self.company_service.get_company_by_name('Company')

        assert 'Company not found' == str(err.value)

    def test_when_company_found_sucessfully(self, app: Flask, company_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(company := CompanyModel(**company_model_data))
            sa.session.commit()

            assert company == self.company_service.get_company_by_name(company_model_data['name'])
