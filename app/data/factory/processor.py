from app.data.factory.factory import DataFactoryType, DataFactory, \
    FromJsonWithValidationToCompanyDataFactory, FromJsonWithValidationToEmployeeDataFactory
from dataclasses import dataclass
from typing import Any, Self


@dataclass
class DataProcessor:
    """
    DataProcessor class for processing data using a specific DataFactory.

    Attributes:
        data_factory (DataFactory): The DataFactory instance used for data processing.
    """

    data_factory: DataFactory

    def __post_init__(self):
        """
        Initialize the DataProcessor after data_factory is set.
        Sets up the loader, validator, and converter using the DataFactory.
        """
        self.loader = self.data_factory.create_loader()
        self.validator = self.data_factory.create_validator()
        self.converter = self.data_factory.create_converter()

    def process(self) -> list[Any]:
        """
        Process the data using the DataFactory.

        Returns:
            List[type]: A list of converted objects.
        """
        loaded = self.loader.load()
        validated = [self.validator.validate(record) for record in loaded]
        return [self.converter.convert(record) for record in validated]

    @classmethod
    def create_processor(cls, factory_type: DataFactoryType, path: str, constraints: dict[str, Any]) -> Self:
        """
        Factory method to create a DataProcessor instance based on the DataFactoryType.

        Args:
            factory_type (DataFactoryType): The type of DataFactory to use.
            path (str): The path to the directory containing JSON files.
            constraints (dict[str, Any]): Dictionary of validation constraints for the data.

        Returns:
            DataProcessor: A new DataProcessor instance based on the specified DataFactoryType.
        """
        if factory_type == DataFactoryType.COMPANY_FACTORY:
            return cls(FromJsonWithValidationToCompanyDataFactory(path, constraints))
        elif factory_type == DataFactoryType.EMPLOYEE_FACTORY:
            return cls(FromJsonWithValidationToEmployeeDataFactory(path, constraints))
