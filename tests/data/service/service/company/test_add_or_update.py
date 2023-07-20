from app.service.service.company import CompanyService
from app.data.model.company import Company
from typing import Any
import pytest


@pytest.fixture
def company_obj(request: Any, company_record_data: dict[str, Any]) -> Company:
    company_record_data['id'] = request.param
    return Company.from_dict(company_record_data)


class TestAddOrUpdate:

    @pytest.mark.parametrize('company_obj', ['10'], indirect=True)
    def test_when_adding_new_record(
            self,
            company_service: CompanyService,
            company_obj: Company
    ) -> None:
        company_service.add_or_update(company_obj)
        assert 3 == len(company_service.find_all())
        assert company_obj == company_service.find_by_id(10)

    @pytest.mark.parametrize('company_obj', ['2'], indirect=True)
    def test_when_updating_existing_record(
            self,
            company_service: CompanyService,
            company_obj: Company
    ) -> None:
        company_service.add_or_update(company_obj)
        assert 2 == len(company_service.find_all())
        assert company_obj == company_service.find_by_id(2)
