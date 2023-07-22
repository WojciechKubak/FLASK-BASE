from app.service.repository.repository import CompanyRepository


def test_find_all(company_repository: CompanyRepository) -> None:
    result = company_repository.find_all()
    assert len(company_repository.companies) == len(result)
