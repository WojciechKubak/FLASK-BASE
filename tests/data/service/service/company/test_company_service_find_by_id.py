from app.service.service.company import CompanyService
import pytest


class TestCompanyServiceFindById:

    def test_when_company_id_is_correct(self, company_service: CompanyService) -> None:
        assert company_service.find_by_id(2)
        assert not company_service.find_by_id(99)

    def test_when_company_id_is_not_correct(self, company_service: CompanyService) -> None:
        with pytest.raises(ValueError) as err:
            company_service.find_by_id(-3)
        assert 'Id must be non-negative number.' == str(err.value)
