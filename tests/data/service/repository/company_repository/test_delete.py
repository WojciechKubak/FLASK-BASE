from app.service.repository.repository import CompanyRepository


def test_when_id_is_present_in_data(company_repository: CompanyRepository) -> None:
    company_repository.delete(2)
    assert 0 == len([c for c in company_repository.companies if c.id_ == 2])
