from app.data.model.employee import Employee
from app.data.factory.factory import \
    FromJsonWithValidationToEmployeeDataFactory, FromJsonWithValidationToCompanyDataFactory
from app.data.layers.validator import CompanyJsonValidator, EmployeeJsonValidator
from typing import Any
import pytest


@pytest.fixture
def company_test_path() -> str:
    return 'tests/example_data/company_data_test.json'


@pytest.fixture
def employee_test_path() -> str:
    return 'tests/example_data/employee_data_test.json'


@pytest.fixture
def empty_data_test_path() -> str:
    return 'tests/example_data/empty_data_test.json'


@pytest.fixture
def company_record_test() -> dict[str, Any]:
    return {
        "id": "2",
        "company_name": "ABC Corporation",
        "street": "123 Main St",
        "city": "New York",
        "postal_code": "10001",
        "state": "NY",
        "country": "USA"
    }


@pytest.fixture
def employee_record_test() -> dict[str, Any]:
    return {
      "id": "0",
      "first_name": "John",
      "last_name": "Doe",
      "position": "Senior Developer",
      "age": "32",
      "employment_tenure": "5",
      "department": "Research and Development",
      "salary": "7000",
      "performance_rating": {
         "efficiency": 4,
         "creativity": 5,
         "communication": 3
      },
      "company": "2"
    }


@pytest.fixture
def employee_test_class_obj(employee_record_test: dict[str, Any]) -> Employee:
    return Employee.from_dict(employee_record_test)


@pytest.fixture
def company_validator_constraints() -> dict[str, Any]:
    return {
        'company_name_regex': r'^[a-zA-Z0-9 .]+$',
        'street_regex': r'^[1-9][0-9]{2} [A-Z][a-z]+(?: [A-Z][a-z]+)*$',
        'city_regex': r'^([A-Z][a-z]+)+(?: ([A-Z][a-z]+)+)*$',
        'state_regex': r'^[A-Z]+$',
        'country_regex': r'^[A-Za-z]+(?: [A-Za-z]+)*$',
    }


@pytest.fixture
def employee_validator_constraints() -> dict[str, Any]:
    return {
        'first_name_regex': r'^[A-Z][a-z]+$',
        'last_name_regex': r'^[A-Z][a-z]+$',
        'position_regex': r'^([A-Z][a-z]+)+(?: ([A-Z][a-z]+)+)*$',
        'department_regex': r'([A-Za-z\s&]+)',
    }


@pytest.fixture
def company_validator_obj(company_validator_constraints: dict[str, Any]) -> CompanyJsonValidator:
    return CompanyJsonValidator(**company_validator_constraints)


@pytest.fixture
def employee_validator_obj(employee_validator_constraints: dict[str, Any]) -> EmployeeJsonValidator:
    return EmployeeJsonValidator(**employee_validator_constraints)


@pytest.fixture
def company_data_factory(
        company_test_path: str,
        company_validator_constraints: dict[str, Any]
) -> FromJsonWithValidationToCompanyDataFactory:
    return FromJsonWithValidationToCompanyDataFactory(company_test_path, company_validator_constraints)


@pytest.fixture
def employee_data_factory(
        employee_test_path: str,
        employee_validator_constraints: dict[str, Any]
) -> FromJsonWithValidationToEmployeeDataFactory:
    return FromJsonWithValidationToEmployeeDataFactory(employee_test_path, employee_validator_constraints)
