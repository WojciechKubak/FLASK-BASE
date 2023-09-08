from app.service.company import CompanyService
from app.model.company import CompanyModel
from app.db.configuration import sa
from typing import Any
from flask import Flask
import pytest


class TestCompanyServiceAddCompany:
    company_service = CompanyService()

    def test_when_company_already_exists(self, app: Flask, company_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(CompanyModel(**company_model_data))
            sa.session.commit()

            with pytest.raises(ValueError) as err:
                self.company_service.add_company(company_model_data)

        assert 'Company already exists' == str(err.value)

    def test_when_company_added_successfully(self, app: Flask, company_model_data: dict[str, Any]) -> None:
        with app.app_context():
            result = self.company_service.add_company(company_model_data)

            assert sa.session.query(CompanyModel).filter_by(name=result.name).first() == result

    def test_when_validation_error_occurs(self, app: Flask, company_model_data: dict[str, Any]) -> None:
        with app.app_context():
            with pytest.raises(ValueError) as err:
                self.company_service.add_company(company_model_data | {'postal_code': 'abcd'})

        assert str(err.value).endswith('does not match condition')
