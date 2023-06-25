from app.data.layers.converter import CompanyConverter
from app.data.organization.company import Company


class TestCompanyConverterConvert:

    def test_if_converter_returns_expected_class_obj(self, company_record_test):
        result = CompanyConverter().convert(company_record_test)
        assert isinstance(result, Company)
