from app.data.layers.loader import JsonLoader
from app.data.layers.validator import CompanyJsonValidator
from app.data.layers.converter import CompanyConverter


class TestCompanyDataFactoryCreateMethods:

    def test_if_create_loader_returns_expected_type(self, company_data_factory):
        assert isinstance(company_data_factory.create_loader(), JsonLoader)

    def test_if_create_validator_returns_expected_type(self, company_data_factory):
        assert isinstance(company_data_factory.create_validator(), CompanyJsonValidator)

    def test_if_create_converter_returns_expected_type(self, company_data_factory):
        assert isinstance(company_data_factory.create_converter(), CompanyConverter)
