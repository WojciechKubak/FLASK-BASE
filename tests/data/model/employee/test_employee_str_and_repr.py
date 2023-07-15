from app.data.model.employee import Employee
from typing import Any


def expected_employee_str_and_repr(company: Any) -> str:
    return f"""ID: 0
First Name: John
Last Name: Doe
Position: Senior Developer
Age: 32
Employment Tenure: 5
Department: Research and Development
Salary: 7000
Performance Rating: {{'efficiency': 4, 'creativity': 5, 'communication': 3}}
Company ID: {company}"""


class TestEmployeeStrAndRepr:

    def test_when_company_attribute_is_id(self, employee_class_obj_with_company_id: Employee) -> None:
        expected = expected_employee_str_and_repr('2')
        assert expected == employee_class_obj_with_company_id.__str__()
        assert expected == employee_class_obj_with_company_id.__repr__()

    def test_when_company_attribute_is_object(self, employee_class_obj_with_company_obj: Employee) -> None:
        expected = expected_employee_str_and_repr('Example company data text')
        assert expected == employee_class_obj_with_company_obj.__str__()
        assert expected == employee_class_obj_with_company_obj.__repr__()
