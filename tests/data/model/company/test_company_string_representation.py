from app.data.model.company import Company
from typing import Any
import pytest


@pytest.fixture
def company_str_repr_without_employee_data() -> str:
    return """ID: 2
Company Name: ABC Corporation
Street: 123 Main St
City: New York
Postal Code: 10001
State: NY
Country: USA
Employees: []"""


@pytest.fixture
def company_str_repr_with_employee_objects() -> str:
    return """ID: 2
Company Name: ABC Corporation
Street: 123 Main St
City: New York
Postal Code: 10001
State: NY
Country: USA
Employees: [employee data, employee data]"""


@pytest.fixture
def company_str_repr_with_employee_ids() -> str:
    return """ID: 2
Company Name: ABC Corporation
Street: 123 Main St
City: New York
Postal Code: 10001
State: NY
Country: USA
Employees: [2, 3, 4]"""


class TestCompanyStrAndRepr:

    def test_when_employees_are_empty(
            self, company_str_repr_without_employees_data: str,
            company_with_no_employees_data: Company
    ) -> None:
        assert company_str_repr_without_employees_data == company_with_no_employees_data.__str__()
        assert company_str_repr_without_employees_data == company_with_no_employees_data.__repr__()

    def test_when_employees_are_objects(
            self, company_str_repr_with_employee_objects: str,
            company_with_employee_objects: Company
    ) -> None:
        assert company_str_repr_with_employee_objects == company_with_employee_objects.__str__()

    def test_when_employees_are_ids(
            self, company_str_repr_with_employee_ids: str,
            company_with_employee_ids: Company
    ) -> None:
        assert company_str_repr_with_employee_ids == company_with_employee_ids.__str__()
