from app.data.layers.validator import CompanyJsonValidator
from typing import Any
import pytest


@pytest.fixture
def company_test_path() -> str:
    return 'tests/example_data/company_data_test.json'


@pytest.fixture
def company_empty_test_path() -> str:
    return 'tests/example_data/company_data_empty_test.json'


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
      "id": 0,
      "first_name": "John",
      "last_name": "Doe",
      "position": "Senior Developer",
      "age": 32,
      "employment_tenure": 5,
      "salary": 7000,
      "performance_rating": {
         "efficiency": 4,
         "creativity": 5,
         "communication": 4
      },
      "company_id": 2
    }


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
def company_validator_obj(company_validator_constraints: dict[str, Any]) -> CompanyJsonValidator:
    return CompanyJsonValidator(**company_validator_constraints)
