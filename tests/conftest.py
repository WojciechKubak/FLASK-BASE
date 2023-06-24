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
        "id": 2,
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
