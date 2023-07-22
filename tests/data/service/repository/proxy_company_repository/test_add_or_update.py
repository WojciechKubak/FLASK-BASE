from app.service.repository.repository import ProxyCompanyRepository, FetchType
import pytest


class TestAddOrUpdate:

    @pytest.mark.parametrize(
        'proxy_company_repository,employee_obj_with_expected_id',
        [(FetchType.LAZY, 10)],
        indirect=True
    )
    def test_adding_new_record(
            self,
            proxy_company_repository: ProxyCompanyRepository,
            employee_obj_with_expected_id
    ) -> None:
        companies_count = len(proxy_company_repository.company_repository.companies)
        proxy_company_repository.add_or_update(employee_obj_with_expected_id)
        assert companies_count + 1 == len(proxy_company_repository.company_repository.companies)
        assert employee_obj_with_expected_id in proxy_company_repository.company_repository.companies

    @pytest.mark.parametrize(
        'proxy_company_repository,employee_obj_with_expected_id',
        [(FetchType.LAZY, 2)],
        indirect=True
    )
    def test_updating_existing_record(
            self,
            proxy_company_repository: ProxyCompanyRepository,
            employee_obj_with_expected_id
    ) -> None:
        companies_count = len(proxy_company_repository.company_repository.companies)
        proxy_company_repository.add_or_update(employee_obj_with_expected_id)
        assert companies_count == len(proxy_company_repository.company_repository.companies)
        assert employee_obj_with_expected_id in proxy_company_repository.company_repository.companies
