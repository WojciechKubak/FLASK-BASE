from app.data.layers.converter import CompanyConverter
from app.data.organization.company import Company
from typing import Any


class TestCompanyConverterConvert:

    def test_if_converter_returns_expected_class_obj(self, company_record_test: dict[str, Any]) -> None:
        result = CompanyConverter().convert(company_record_test)
        assert isinstance(result, Company)
