from app.service.company import CompanyService
from app.model.company import CompanyModel
from app.db.configuration import sa
from typing import Any
from flask import Flask
import pytest


class TestCompanyServiceUpdateCompany:
    company_service = CompanyService()

    def test_when_company_does_not_exist(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(ValueError) as err:
                self.company_service.update_company({'name': 'Company'})

        assert 'Company not found' == str(err.value)

    def test_when_updated_succesfully(self, app: Flask, company_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(CompanyModel(**company_model_data))
            sa.session.commit()

            result = self.company_service.update_company(company_model_data | {'postal_code': '54321'})

            assert sa.session.query(CompanyModel).filter_by(name=company_model_data['name']).first() == result

    def test_when_validation_error_occurs(self, app: Flask, company_model_data: dict[str, Any]) -> None:
        with app.app_context():
            sa.session.add(CompanyModel(**company_model_data))
            sa.session.commit()

            with pytest.raises(ValueError) as err:
                self.company_service.update_company(company_model_data | {'postal_code': '1234a'})

        assert str(err.value).endswith('does not match condition')
