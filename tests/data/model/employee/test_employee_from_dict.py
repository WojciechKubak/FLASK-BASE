from app.data.model.employee import Employee
from decimal import Decimal
from typing import Any


def test_basic_type_conversion(employee_record_test: dict[str, Any]) -> None:
    result = Employee.from_dict(employee_record_test)
    assert isinstance(result, Employee)
    assert 0 == result.id_
    assert 32 == result.age
    assert 2 == result.company
    assert Decimal('7000') == result.salary
