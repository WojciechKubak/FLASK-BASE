from app.data.models.employee import Employee
from decimal import Decimal
from typing import Any


def test_when_data_is_correct(employee_record_test: dict[str, Any]) -> None:
    result = Employee.from_dict(employee_record_test)
    assert isinstance(result, Employee)
    assert Decimal('7000') == result.salary
