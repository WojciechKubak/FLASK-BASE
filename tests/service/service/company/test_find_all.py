from app.service.service.company import CompanyService


def test_find_all(company_service: CompanyService) -> None:
    result = company_service.find_all()
    assert company_service.company_repository.companies == result
