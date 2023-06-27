from app.data.factory.factory import DataFactory
from app.data.factory.processor import DataProcessor
from app.data.layers.loader import Loader, JsonLoader
from app.data.layers.validator import Validator, CompanyJsonValidator
from app.data.layers.converter import Converter, CompanyConverter
from unittest.mock import MagicMock
import pytest


class MockDataProcessor(DataFactory):

    def create_loader(self) -> Loader:
        json_loader = JsonLoader('')
        json_loader.load = MagicMock(return_value=[])
        return json_loader

    def create_validator(self) -> Validator:
        company_validator = CompanyJsonValidator('', '', '', '', '')
        company_validator.validate = MagicMock(return_value=[])
        return company_validator

    def create_converter(self) -> Converter:
        company_converter = CompanyConverter()
        company_converter.convert = MagicMock(return_value=[])
        return company_converter


@pytest.mark.skip('This is not prepared to be tested.')
def test_when_company_data_processor_works_correctly():
    data_processor = DataProcessor(MockDataProcessor())
    assert [] == data_processor.process()
