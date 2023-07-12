from app.data.models.employee import Employee
from typing import Any
import pytest


@pytest.fixture
def employee_str_repr() -> str:
    return """ID: 0
First Name: John
Last Name: Doe
Position: Senior Developer
Age: 32
Employment Tenure: 5
Department: Research and Development
Salary: 7000
Performance Rating: {'efficiency': 4, 'creativity': 5, 'communication': 4}
Company ID: 2"""


def test_employee_str_and_repr(employee_record_test: dict[str, Any], employee_str_repr: str) -> None:
    employee = Employee.from_dict(employee_record_test)
    assert employee_str_repr == str(employee)
    assert employee_str_repr == repr(employee)
