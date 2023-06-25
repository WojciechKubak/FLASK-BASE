from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Any, Callable
import re


@dataclass
class Validator(ABC):
    _errors: dict[str, str] = field(default_factory=dict, init=False)

    @abstractmethod
    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        pass

    def errors_to_str(self) -> str:
        return ', '.join([f'{key}: {message}' for key, message in self._errors.items()])

    @staticmethod
    def validate_value(data: dict[str, Any], key: str, constraint: Callable) -> str:
        if not (to_validate := data.get(key)):
            return 'key not found'
        if constraint(to_validate):
            return ''
        return 'does not match condition'

    @staticmethod
    def match_regex(text: str, regex: str) -> bool:
        return re.match(regex, text) is not None

    @staticmethod
    def match_if_string_contains_non_negative_number(text: str, expected_type: type) -> bool:
        if expected_type not in [int, float]:
            raise TypeError('Incorrect type provided.')
        data_type_regex = {
            int: r'^\d+$',
            float: r'^\d+(\.\d+)?$'
        }
        return re.match(data_type_regex[expected_type], text) is not None


@dataclass
class CompanyJsonValidator(Validator):
    company_name_regex: str
    street_regex: str
    city_regex: str
    state_regex: str
    country_regex: str

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        constraints = {
            'id': lambda x: self.match_if_string_contains_non_negative_number(x, int),
            'company_name': lambda x: self.match_regex(x, self.company_name_regex),
            'street': lambda x: self.match_regex(x, self.street_regex),
            'postal_code': lambda x: self.match_if_string_contains_non_negative_number(x, int),
            'city': lambda x: self.match_regex(x, self.city_regex),
            'state': lambda x: self.match_regex(x, self.state_regex),
            'country': lambda x: self.match_regex(x, self.country_regex),
        }
        for key, constraint in constraints.items():
            if result := self.validate_value(data, key, constraint):
                self._errors[key] = result
        if len(self._errors) > 0:
            raise ValueError(self.errors_to_str())
        return data


@dataclass
class EmployeeJsonValidator(Validator):
    first_name_regex: str
    last_name_regex: str
    position_regex: str

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        constraints = {
            'id': lambda x: self.match_if_string_contains_non_negative_number(x, int),
            'first_name': lambda x: self.match_regex(x, self.first_name_regex),
            'last_name': lambda x: self.match_regex(x, self.last_name_regex),
            'position': lambda x: self.match_regex(x, self.position_regex),
            'age': lambda x: self.match_if_string_contains_non_negative_number(x, int),
            'employment_tenure': lambda x: self.match_if_string_contains_non_negative_number(x, int),
            'salary': lambda x: self.match_if_string_contains_non_negative_number(x, float),
            'performance_rating': lambda x: all(
                self.match_if_string_contains_non_negative_number(str(y), int) for y in x.values()),
            'company_id': lambda x: self.match_if_string_contains_non_negative_number(x, int),
        }
        for key, constraint in constraints.items():
            if result := self.validate_value(data, key, constraint):
                self._errors[key] = result
        if len(self._errors) > 0:
            raise ValueError(self.errors_to_str())
        return data
