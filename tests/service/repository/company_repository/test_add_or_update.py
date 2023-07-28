from app.service.repository.repository import CompanyRepository
from app.data.model.company import Company
from typing import Any
import pytest


@pytest.fixture
def company_obj(request: Any, company_record_data: dict[str, Any]) -> Company:
    company_record_data['id'] = request.param
    return Company.from_dict(company_record_data)


@pytest.mark.parametrize('company_obj', ['10', '2'], indirect=True)
def test_when_adding_new_record(
        company_repository: CompanyRepository,
        company_obj: Company
) -> None:
    company_repository.add_or_update(company_obj)
    assert company_obj in company_repository.companies
