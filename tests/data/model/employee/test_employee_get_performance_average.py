from app.data.model.employee import Employee
from typing import Any


def test_employee_get_performance_average_works_correctly(employee_record_test: dict[str, Any]) -> None:
    employee_record_test['performance_rating'] = {
         "efficiency": 4,
         "creativity": 5,
         "communication": 3
    }
    employee = Employee.from_dict(employee_record_test)
    assert 4. == employee.get_performance_average()
