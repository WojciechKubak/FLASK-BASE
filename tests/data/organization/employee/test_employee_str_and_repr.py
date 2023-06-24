from app.data.organization.employee import Employee
from typing import Any


class TestEmployeeStrAndRepr:

    def test_employee_str_and_repr(self, employee_record_test: dict[str, Any]) -> None:
        employee = Employee.from_dict(employee_record_test)
        expected_result = """
            ID: 0
            First Name: John
            Last Name: Doe
            Position: Senior Developer
            Age: 32
            Employment Tenure: 5
            Salary: 7000
            Performance Rating: {'efficiency': 4, 'creativity': 5, 'communication': 4}
            Company ID: 2
        """
        assert expected_result == str(employee)
        assert expected_result == repr(employee)