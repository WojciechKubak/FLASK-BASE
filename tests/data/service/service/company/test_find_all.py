from app.service.service.company import CompanyService


def test_find_all(company_service: CompanyService) -> None:
    result = company_service.find_all()
    assert 4 == len(result)
    assert 2 == result[0].id_
    assert 1 == result[1].id_
