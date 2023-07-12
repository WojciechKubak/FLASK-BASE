from app.data.models.company import Company
from typing import Any
import pytest


@pytest.fixture
def company_str_repr() -> str:
    return """ID: 2
Company Name: ABC Corporation
Street: 123 Main St
City: New York
Postal Code: 10001
State: NY
Country: USA"""


def test_company_str_and_repr(company_record_test: dict[str, Any], company_str_repr: str) -> None:
    company = Company.from_dict(company_record_test)
    assert company_str_repr == str(company)
    assert company_str_repr == repr(company)
