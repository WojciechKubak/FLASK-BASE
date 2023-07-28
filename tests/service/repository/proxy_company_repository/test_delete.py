from app.service.repository.repository import ProxyCompanyRepository, FetchType
import pytest


@pytest.mark.parametrize('proxy_company_repository', [FetchType.LAZY], indirect=True)
def test_delete(proxy_company_repository: ProxyCompanyRepository) -> None:
    proxy_company_repository.delete(2)
    assert 0 == len([c for c in proxy_company_repository.company_repository.companies if c.id_ == 2])
