from app.data.layers.loader import Loader, JsonLoader
from app.data.layers.validator import Validator, CompanyJsonValidator, EmployeeJsonValidator
from app.data.layers.converter import Converter, CompanyConverter, EmployeeConverter
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any


class DataFactoryType(Enum):
    COMPANY_FACTORY = auto()
    EMPLOYEE_FACTORY = auto()


@dataclass
class DataFactory(ABC):

    @abstractmethod
    def create_loader(self) -> Loader:
        pass

    @abstractmethod
    def create_validator(self) -> Validator:
        pass

    @abstractmethod
    def create_converter(self) -> Converter:
        pass


@dataclass
class FromJsonWithValidationToCompanyDataFactory(DataFactory):
    path: str
    constraints: dict[str, Any]

    def create_loader(self) -> Loader:
        return JsonLoader(self.path)

    def create_validator(self) -> Validator:
        return CompanyJsonValidator(**self.constraints)

    def create_converter(self) -> Converter:
        return CompanyConverter()


@dataclass
class FromJsonWithValidationToEmployeeDataFactory(DataFactory):
    path: str
    constraints: dict[str, Any]

    def create_loader(self) -> Loader:
        return JsonLoader(self.path)

    def create_validator(self) -> Validator:
        return EmployeeJsonValidator(**self.constraints)

    def create_converter(self) -> Converter:
        return EmployeeConverter()


