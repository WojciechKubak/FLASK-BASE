from app.data.layers.loader import Loader, JsonLoader
from app.data.layers.validator import Validator, CompanyJsonValidator, EmployeeJsonValidator
from app.data.layers.converter import Converter, CompanyConverter, EmployeeConverter
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any


class DataFactoryType(Enum):
    """
    Enumeration of data factory types.

    Attributes:
        COMPANY_FACTORY (DataFactoryType): Represents a data factory for creating Company objects.
        EMPLOYEE_FACTORY (DataFactoryType): Represents a data factory for creating Employee objects.
    """
    COMPANY_FACTORY = auto()
    EMPLOYEE_FACTORY = auto()


@dataclass
class DataFactory(ABC):
    """
    Abstract base class for data factories.

    Methods:
        create_loader() -> Loader: Abstract method to create a data loader instance.
        create_validator() -> Validator: Abstract method to create a data validator instance.
        create_converter() -> Converter: Abstract method to create a data converter instance.
    """

    @abstractmethod
    def create_loader(self) -> Loader:
        """
        Abstract method to create a data loader instance.

        Returns:
            Loader: A data loader instance.
        """
        pass

    @abstractmethod
    def create_validator(self) -> Validator:
        """
        Abstract method to create a data validator instance.

        Returns:
            Validator: A data validator instance.
        """
        pass

    @abstractmethod
    def create_converter(self) -> Converter:
        """
        Abstract method to create a data converter instance.

        Returns:
            Converter: A data converter instance.
        """
        pass


@dataclass
class FromJsonWithValidationToCompanyDataFactory(DataFactory):
    """
    Data factory for creating objects related to Company data from JSON with validation.

    Attributes:
        path (str): The path to the directory containing JSON files.
        constraints (dict[str, Any]): Dictionary of validation constraints for Company data.
    """

    path: str
    constraints: dict[str, Any]

    def create_loader(self) -> Loader:
        """
        Create a JSON loader instance for Company data.

        Returns:
            Loader: A JSON loader instance.
        """
        return JsonLoader(self.path)

    def create_validator(self) -> Validator:
        """
        Create a Company JSON validator instance with the specified constraints.

        Returns:
            Validator: A Company JSON validator instance.
        """
        return CompanyJsonValidator(**self.constraints)

    def create_converter(self) -> Converter:
        """
        Create a Company data converter instance.

        Returns:
            Converter: A Company data converter instance.
        """
        return CompanyConverter()


@dataclass
class FromJsonWithValidationToEmployeeDataFactory(DataFactory):
    """
    Data factory for creating objects related to Employee data from JSON with validation.

    Attributes:
        path (str): The path to the directory containing JSON files.
        constraints (dict[str, Any]): Dictionary of validation constraints for Employee data.
    """

    path: str
    constraints: dict[str, Any]

    def create_loader(self) -> Loader:
        """
        Create a JSON loader instance for Employee data.

        Returns:
            Loader: A JSON loader instance.
        """
        return JsonLoader(self.path)

    def create_validator(self) -> Validator:
        """
        Create an Employee JSON validator instance with the specified constraints.

        Returns:
            Validator: An Employee JSON validator instance.
        """
        return EmployeeJsonValidator(**self.constraints)

    def create_converter(self) -> Converter:
        """
        Create an Employee data converter instance.

        Returns:
            Converter: An Employee data converter instance.
        """
        return EmployeeConverter()
