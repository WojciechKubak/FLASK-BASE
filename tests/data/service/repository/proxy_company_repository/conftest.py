from app.service.repository.repository import CompanyRepository, EmployeeRepository, ProxyCompanyRepository
from typing import Any
import pytest


@pytest.fixture
def proxy_company_repository(
        request: Any,
        company_repository: CompanyRepository,
        employee_repository: EmployeeRepository
) -> ProxyCompanyRepository:
    return ProxyCompanyRepository(company_repository, employee_repository, request.param)
