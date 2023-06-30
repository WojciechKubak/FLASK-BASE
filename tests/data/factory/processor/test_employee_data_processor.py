from app.data.layers.loader import JsonLoader
from app.data.layers.validator import EmployeeJsonValidator
from app.data.layers.converter import EmployeeConverter
from app.data.factory.processor import DataProcessor
from app.data.organization.employee import Employee
from unittest.mock import MagicMock
from typing import Any


def test_when_employee_data_processor_works_correctly(
        employee_test_path: str,
        employee_validator_constraints: dict[str, Any]
) -> None:
    data_factory = MagicMock()
    data_factory.create_loader.return_value = JsonLoader(employee_test_path)
    data_factory.create_validator.return_value = EmployeeJsonValidator(**employee_validator_constraints)
    data_factory.create_converter.return_value = EmployeeConverter()
    result = DataProcessor(data_factory).process()
    assert 2 == len(result)
    assert all(isinstance(obj, Employee) for obj in result)
