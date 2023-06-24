from app.data.organization.company import Company
from typing import Any
import logging


class TestCompanyStrAndRepr:

    def test_company_str_and_repr(self, company_record_test: dict[str, Any]) -> None:
        company = Company.from_dict(company_record_test)
        expected_result = f"""
            ID: 2
            Company Name: ABC Corporation
            Street: 123 Main St
            City: New York
            Postal Code: 10001
            State: NY
            Country: USA
        """
        assert expected_result == str(company)
        assert expected_result == repr(company)
