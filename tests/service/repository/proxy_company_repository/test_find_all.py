from app.service.repository.repository import ProxyCompanyRepository, FetchType
from app.data.model.employee import Employee
from itertools import chain
import pytest


class TestFindAll:

    @pytest.mark.parametrize('proxy_company_repository', [FetchType.LAZY], indirect=True)
    def test_connection_with_repositories(self, proxy_company_repository: ProxyCompanyRepository) -> None:
        result = proxy_company_repository.find_all()
        assert len(proxy_company_repository.company_repository.companies) == len(result)
        employee_ids_pool = [e.id_ for e in proxy_company_repository.employee_repository.employees]
        result_employee_ids = list(set(chain(*[r.employees for r in result])))
        assert sorted(employee_ids_pool) == sorted(result_employee_ids)

    @pytest.mark.parametrize('proxy_company_repository', [FetchType.LAZY], indirect=True)
    def test_when_fetch_type_is_lazy(self, proxy_company_repository: ProxyCompanyRepository) -> None:
        result = proxy_company_repository.find_all()
        assert isinstance(result[0].employees, list)
        assert isinstance(result[0].employees[0], int)

    @pytest.mark.parametrize('proxy_company_repository', [FetchType.EAGER], indirect=True)
    def test_when_fetch_type_is_eager(self, proxy_company_repository: ProxyCompanyRepository) -> None:
        result = proxy_company_repository.find_all()
        assert isinstance(result[0].employees, list)
        assert isinstance(result[0].employees[0], Employee)
