from app.data.layers.loader import JsonLoader
from app.data.layers.validator import CompanyJsonValidator
from app.data.layers.converter import CompanyConverter
from app.data.factory.processor import DataProcessor
from app.data.model.company import Company
from unittest.mock import MagicMock
from typing import Any


def test_when_company_data_processor_works_correctly(
        company_test_path: str,
        company_validator_constraints: dict[str, Any]
) -> None:
    data_factory = MagicMock()
    data_factory.create_loader.return_value = JsonLoader(company_test_path)
    data_factory.create_validator.return_value = CompanyJsonValidator(**company_validator_constraints)
    data_factory.create_converter.return_value = CompanyConverter()
    result = DataProcessor(data_factory).process()
    assert 2 == len(result)
    assert all(isinstance(obj, Company) for obj in result)
