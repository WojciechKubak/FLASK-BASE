from app.service.service.company import CompanyService
import pytest


class TestDelete:

    def test_when_id_is_not_correct(self, company_service: CompanyService) -> None:
        with pytest.raises(ValueError) as err:
            company_service.delete(-99)
        assert 'Id must be non-negative number.' == str(err.value)

    def test_when_id_is_present_in_data(self, company_service: CompanyService) -> None:
        record_counter = len(company_service.find_all())
        company_service.delete(2)
        assert not company_service.find_by_id(2)
        assert record_counter - 1 == len(company_service.find_all())

    def test_when_id_is_not_present_in_data(self, company_service: CompanyService) -> None:
        record_counter = len(company_service.find_all())
        company_service.delete(999)
        assert record_counter == len(company_service.find_all())
