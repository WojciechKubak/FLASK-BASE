from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Any, Callable
import re


@dataclass
class Validator(ABC):
    """
    Abstract base class for data validators.

    Attributes:
        _errors (dict[str, str]): Dictionary to store validation errors.
    """

    _errors: dict[str, str] = field(default_factory=dict, init=False)

    @abstractmethod
    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Abstract method to be implemented by subclasses.
        Performs data validation and returns the validated data.

        Args:
            data (dict[str, Any]): The data to be validated.

        Returns:
            dict[str, Any]: The validated data.

        Raises:
            ValueError: If validation fails and there are errors in the data.
        """
        pass

    def errors_to_str(self) -> str:
        """
        Convert validation errors to a human-readable string.

        Returns:
            str: A string containing the list of validation errors.
        """
        return ', '.join([f'{key} {message}' for key, message in self._errors.items()])

    @staticmethod
    def validate_value(data: dict[str, Any], key: str, constraint: Callable) -> str:
        """
         Validate a specific value in the data dictionary based on the given constraint function.

         Args:
             data (dict[str, Any]): The data dictionary to validate.
             key (str): The key representing the value to validate.
             constraint (Callable): The constraint function to apply on the value.

         Returns:
             str: An empty string if the value satisfies the constraint, otherwise an error message.
         """
        if not (to_validate := data.get(key)):
            return 'field required'
        if constraint(to_validate):
            return ''
        return 'does not match condition'

    @staticmethod
    def match_regex(text: str, regex: str) -> bool:
        """
        Check if a text matches the given regular expression.

        Args:
            text (str): The text to match against the regular expression.
            regex (str): The regular expression pattern.

        Returns:
            bool: True if the text matches the regular expression, False otherwise.
        """
        return re.match(regex, text) is not None

    @staticmethod
    def match_if_string_contains_non_negative_number(text: str, expected_type: type) -> bool:
        """
        Check if a text contains a non-negative number of the specified type.

        Args:
            text (str): The text to check for a non-negative number.
            expected_type (type): The expected type of the number (int or float).

        Returns:
            bool: True if the text contains a non-negative number of the specified type, False otherwise.

        Raises:
            TypeError: If an incorrect type is provided.
        """
        if expected_type not in [int, float]:
            raise TypeError('Incorrect type provided.')
        data_type_regex = {
            int: r'^\d+$',
            float: r'^\d+(\.\d+)?$'
        }
        return re.match(data_type_regex[expected_type], text) is not None


@dataclass
class CompanyJsonValidator(Validator):
    """
    Data validator for company JSON data.

    Attributes:
        company_name_regex (str): Regular expression pattern for validating company names.
        street_regex (str): Regular expression pattern for validating street names.
        city_regex (str): Regular expression pattern for validating city names.
        state_regex (str): Regular expression pattern for validating state names.
        country_regex (str): Regular expression pattern for validating country names.
    """

    company_name_regex: str
    street_regex: str
    city_regex: str
    state_regex: str
    country_regex: str

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Validate the company JSON data.

        Args:
            data (dict[str, Any]): The company data to be validated.

        Returns:
            dict[str, Any]: The validated company data.

        Raises:
            ValueError: If validation fails and there are errors in the data.
        """
        constraints = {
            'name': lambda x: self.match_regex(x, self.company_name_regex),
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
    """
    Data validator for employee JSON data.

    Attributes:
        full_name_regex (str): Regular expression pattern for validating employee full names.
        position_regex (str): Regular expression pattern for validating employee positions.
        department_regex (str): Regular expression pattern for validating employee departments.
    """
    full_name_regex: str
    position_regex: str
    department_regex: str

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Validate the employee JSON data.

        Args:
            data (dict[str, Any]): The employee data to be validated.

        Returns:
            dict[str, Any]: The validated employee data.

        Raises:
            ValueError: If validation fails and there are errors in the data.
        """
        constraints = {
            'full_name': lambda x: self.match_regex(x, self.full_name_regex),
            'position': lambda x: self.match_regex(x, self.position_regex),
            'age': lambda x: self.match_if_string_contains_non_negative_number(str(x), int),
            'employment_tenure': lambda x: self.match_if_string_contains_non_negative_number(str(x), int),
            'department': lambda x: self.match_regex(x, self.department_regex),
            'salary': lambda x: self.match_if_string_contains_non_negative_number(str(x), float),
            'performance_rating': lambda x: all(
                self.match_if_string_contains_non_negative_number(str(y), int) for y in x.values()),
            'company_id': lambda x: self.match_if_string_contains_non_negative_number(str(x), int),
        }

        for key, constraint in constraints.items():
            if result := self.validate_value(data, key, constraint):
                self._errors[key] = result
        if len(self._errors) > 0:
            raise ValueError(self.errors_to_str())

        return data


@dataclass
class UserJsonValidator(Validator):
    """
    Data validator for user JSON data.

    Attributes:
        username_regex (str): Regular expression pattern for validating usernames.
        email_regex (str): Regular expression pattern for validating email addresses.
        password_regex (str): Regular expression pattern for validating passwords.
    """

    username_regex: str
    email_regex: str
    password_regex: str

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Validate the user JSON data.

        Args:
            data (dict[str, Any]): The user data to be validated.

        Returns:
            dict[str, Any]: The validated user data.

        Raises:
            ValueError: If validation fails and there are errors in the data.
        """
        constraints = {
            'username': lambda x: self.match_regex(x, self.username_regex),
            'email': lambda x: self.match_regex(x, self.email_regex),
            'password': lambda x: self.match_regex(x, self.password_regex),
        }

        for key, constraint in constraints.items():
            if result := self.validate_value(data, key, constraint):
                self._errors[key] = result
        if len(self._errors) > 0:
            raise ValueError(self.errors_to_str())

        return data
