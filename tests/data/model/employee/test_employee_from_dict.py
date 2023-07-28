from app.data.model.employee import Employee
from decimal import Decimal
from typing import Any


def test_employee_from_dict_conversion(employee_record_data: dict[str, Any]) -> None:
    result = Employee.from_dict(employee_record_data)
    assert isinstance(result.id_, int)
    assert isinstance(result.age, int)
    assert isinstance(result.company, int)
    assert isinstance(result.salary, Decimal)
