from app.data.model.employee import Employee
from decimal import Decimal
from typing import Any


def test_employee_from_dict_conversion(employee_record_data: dict[str, Any]) -> None:
    result = Employee.from_dict(employee_record_data)
    assert isinstance(result, Employee)
    assert 0 == result.id_
    assert 32 == result.age
    assert 2 == result.company
    assert Decimal('7000') == result.salary
