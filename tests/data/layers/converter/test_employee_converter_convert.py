from app.data.layers.converter import EmployeeConverter
from app.data.organization.employee import Employee
from typing import Any


def test_if_employee_converter_returns_expected_class_obj(employee_record_test: dict[str, Any]) -> None:
    result = EmployeeConverter().convert(employee_record_test)
    assert isinstance(result, Employee)
