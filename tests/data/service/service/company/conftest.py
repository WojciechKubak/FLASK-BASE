from app.service.repository.repository import CompanyRepository
from app.service.service.company import CompanyService
from typing import Any
import pytest


@pytest.fixture
def company_repository(company_test_path: str, company_validator_constraints: dict[str, Any]) -> CompanyRepository:
    return CompanyRepository(company_test_path, company_validator_constraints)


@pytest.fixture
def company_service(company_repository: CompanyRepository) -> CompanyService:
    return CompanyService(company_repository)
