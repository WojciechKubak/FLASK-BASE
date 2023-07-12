from app.data.models.company import Company
from app.data.models.employee import Employee
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class Converter(ABC):

    @abstractmethod
    def convert(self, data: dict[str, Any]) -> type:
        pass


@dataclass
class CompanyConverter(Converter):

    def convert(self, data: dict[str, Any]) -> type:
        return Company.from_dict(data)


@dataclass
class EmployeeConverter(Converter):

    def convert(self, data: dict[str, Any]) -> type:
        return Employee.from_dict(data)
