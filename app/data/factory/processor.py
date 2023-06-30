from app.data.factory.factory import DataFactoryType, DataFactory, \
    FromJsonWithValidationToCompanyDataFactory, FromJsonWithValidationToEmployeeDataFactory
from dataclasses import dataclass
from typing import Self, Any


@dataclass
class DataProcessor:
    data_factory: DataFactory

    def __post_init__(self):
        self.loader = self.data_factory.create_loader()
        self.validator = self.data_factory.create_validator()
        self.converter = self.data_factory.create_converter()

    def process(self) -> list[type]:
        loaded = self.loader.load()
        validated = [self.validator.validate(record) for record in loaded]
        return [self.converter.convert(record) for record in validated]

    @classmethod
    def create_processor(cls: Self, factory_type: DataFactoryType, path: str, constraints: dict[str, Any]) -> Self:
        match factory_type:
            case DataFactoryType.COMPANY_FACTORY:
                return cls(FromJsonWithValidationToCompanyDataFactory(path, constraints))
            case DataFactoryType.EMPLOYEE_FACTORY:
                return cls(FromJsonWithValidationToEmployeeDataFactory(path, constraints))
