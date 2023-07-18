from app.data.model.employee import Employee
from typing import Any
import pytest


@pytest.mark.parametrize(
    'test_input,expected', [
        ({"efficiency": 4, "creativity": 5, "communication": 3}, 4.),
        ({"efficiency": 6, "creativity": 4}, 5.),
        ({"efficiency": 0}, 0),
        ({}, None)
    ]
)
def test_employee_get_performance_average(
        employee_record_data: dict[str, Any],
        test_input: dict[str, Any],
        expected: Any
) -> None:
    employee_record_data['performance_rating'] = test_input
    employee = Employee.from_dict(employee_record_data)
    assert expected == employee.get_performance_average()
