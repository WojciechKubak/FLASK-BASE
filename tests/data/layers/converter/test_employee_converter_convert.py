from app.data.layers.converter import EmployeeConverter
from app.data.organization.employee import Employee
from typing import Any


class TestEmployeeConverterConvert:

    def test_if_converter_returns_expected_class_obj(self, employee_record_test: dict[str, Any]) -> None:
        result = EmployeeConverter().convert(employee_record_test)
        assert isinstance(result, Employee)
