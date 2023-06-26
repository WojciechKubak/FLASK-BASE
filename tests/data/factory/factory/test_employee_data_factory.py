from app.data.layers.loader import JsonLoader
from app.data.layers.validator import EmployeeJsonValidator
from app.data.layers.converter import EmployeeConverter


class TestEmployeeDataFactoryCreateMethods:

    def test_if_create_loader_returns_expected_type(self, employee_data_factory):
        assert isinstance(employee_data_factory.create_loader(), JsonLoader)

    def test_if_create_validator_returns_expected_type(self, employee_data_factory):
        assert isinstance(employee_data_factory.create_validator(), EmployeeJsonValidator)

    def test_if_create_converter_returns_expected_type(self, employee_data_factory):
        assert isinstance(employee_data_factory.create_converter(), EmployeeConverter)
