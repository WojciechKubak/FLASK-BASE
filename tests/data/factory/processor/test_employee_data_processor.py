from app.data.layers.loader import JsonLoader
from app.data.layers.validator import EmployeeJsonValidator
from app.data.layers.converter import EmployeeConverter
from app.data.factory.processor import DataProcessor
from app.data.factory.factory import DataFactory
from app.data.model.employee import Employee
from unittest.mock import MagicMock
from typing import Any
import pytest


@pytest.fixture
def employee_data_factory_mock(employee_test_path: str, employee_validator_constraints: dict[str, Any]) -> MagicMock:
    data_factory = MagicMock()
    data_factory.create_loader.return_value = JsonLoader(employee_test_path)
    data_factory.create_validator.return_value = EmployeeJsonValidator(**employee_validator_constraints)
    data_factory.create_converter.return_value = EmployeeConverter()
    return data_factory


def test_when_employee_data_processor_works_correctly(employee_data_factory_mock: DataFactory) -> None:
    result = DataProcessor(employee_data_factory_mock).process()
    assert 4 == len(result)
    assert all(isinstance(obj, Employee) for obj in result)
