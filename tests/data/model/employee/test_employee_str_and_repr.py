from app.data.model.employee import Employee
import pytest


@pytest.fixture
def employee_str_and_repr() -> str:
    return """ID: 0
First Name: John
Last Name: Doe
Position: Senior Developer
Age: 32
Employment Tenure: 5
Department: Research and Development
Salary: 7000
Performance Rating: {'efficiency': 4, 'creativity': 5, 'communication': 3}
Company ID: 2"""


def test_employee_str_and_repr(employee_obj: Employee, employee_str_and_repr: str) -> None:
    assert employee_str_and_repr == employee_obj.__str__()
    assert employee_str_and_repr == employee_obj.__repr__()
