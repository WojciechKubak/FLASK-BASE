from app.service.service.company import CompanyService


def test_company_service_find_all(company_service: CompanyService) -> None:
    result = company_service.find_all()
    assert 2 == len(result)
    assert result[0].id_ == 2
    assert result[1].id_ == 1
