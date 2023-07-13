from app.data.layers.converter import CompanyConverter
from app.data.model.company import Company
from typing import Any


def test_if_company_converter_returns_expected_class_obj(company_record_test: dict[str, Any]) -> None:
    result = CompanyConverter().convert(company_record_test)
    assert isinstance(result, Company)
