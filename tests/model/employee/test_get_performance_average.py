from app.model.employee import EmployeeModel
import pytest


@pytest.mark.parametrize(
    'test_input,expected', [
        ({"efficiency": 4, "creativity": 5, "communication": 3}, 4.),
        ({"efficiency": 6, "creativity": 4}, 5.),
        ({"efficiency": 0}, 0),
        ({}, None)
    ]
)
def test_employee_model_get_performance_average(test_input: dict[str, int], expected: float) -> None:
    employee = EmployeeModel(full_name='Employee', performance_rating=test_input)
    assert expected == employee.get_performance_average()
