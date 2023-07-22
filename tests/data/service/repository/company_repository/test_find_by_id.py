from app.service.repository.repository import CompanyRepository


def test_find_by_id(company_repository: CompanyRepository) -> None:
    result = company_repository.find_by_id(2)
    assert result in company_repository.companies
