from app.data.model.company import Company
from typing import Any


def test_when_data_is_correct(company_record_test: dict[str, Any]) -> None:
    result = Company.from_dict(company_record_test)
    assert isinstance(result, Company)
