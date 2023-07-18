from app.data.model.employee import Employee
from typing import Any


def test_employee_to_dict_conversion(employee_record_data: dict[str, Any]) -> None:
    employee = Employee.from_dict(employee_record_data)
    result = employee.to_dict()
    assert len(employee_record_data) == len(result)
    assert 2 == result['company']
    assert 'id' in result
