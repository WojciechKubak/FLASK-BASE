from app.service.repository.repository import ProxyCompanyRepository, FetchType
from app.data.model.employee import Employee
import logging
import pytest


class TestFindById:

    @pytest.mark.parametrize('proxy_company_repository', [FetchType.LAZY], indirect=True)
    def test_connection_with_repositories(self, proxy_company_repository: ProxyCompanyRepository) -> None:
        result = proxy_company_repository.find_by_id(2)
        assert result.id_ in [company.id_ for company in proxy_company_repository.company_repository.companies]
        employee_ids_pool = [e.id_ for e in proxy_company_repository.employee_repository.employees]
        assert all([employee_id in employee_ids_pool for employee_id in result.employees])

    @pytest.mark.parametrize('proxy_company_repository', [FetchType.LAZY], indirect=True)
    def test_when_fetch_type_is_lazy(self, proxy_company_repository: ProxyCompanyRepository) -> None:
        result = proxy_company_repository.find_by_id(2)
        logging.info(result)
        assert isinstance(result.employees, list)
        assert isinstance(result.employees[0], int)

    @pytest.mark.parametrize('proxy_company_repository', [FetchType.EAGER], indirect=True)
    def test_when_fetch_type_is_eager(self, proxy_company_repository: ProxyCompanyRepository) -> None:
        result = proxy_company_repository.find_by_id(2)
        assert isinstance(result.employees, list)
        assert isinstance(result.employees[0], Employee)
