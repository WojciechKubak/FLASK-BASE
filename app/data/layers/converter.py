from app.data.model.company import Company
from app.data.model.employee import Employee
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class Converter(ABC):
    """
    Abstract base class for data converters.
    """

    @abstractmethod
    def convert(self, data: dict[str, Any]) -> type:
        """
        Abstract method to be implemented by subclasses.
        Converts the provided data dictionary into an object of the specified type.

        Args:
            data (dict[str, Any]): The data dictionary to be converted.

        Returns:
            type: An object of the specified type containing the converted data.
        """
        pass


@dataclass
class CompanyConverter(Converter):
    """
    Data converter for Company objects.
    """

    def convert(self, data: dict[str, Any]) -> Company:
        """
        Convert the provided data dictionary into a Company object.

        Args:
            data (dict[str, Any]): The data dictionary to be converted.

        Returns:
            Company: A Company object containing the converted data.
        """
        return Company.from_dict(data)


@dataclass
class EmployeeConverter(Converter):
    """
    Data converter for Employee objects.
    """

    def convert(self, data: dict[str, Any]) -> Employee:
        """
        Convert the provided data dictionary into an Employee object.

        Args:
            data (dict[str, Any]): The data dictionary to be converted.

        Returns:
            Employee: An Employee object containing the converted data.
        """
        return Employee.from_dict(data)
