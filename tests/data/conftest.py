from typing import Any
import pytest


@pytest.fixture
def company_json_data() -> dict[str, Any]:
    return {
        "name": "XYZ Inc.",
        "street": "456 Elm St",
        "city": "City",
        "postal_code": "12345",
        "state": "NY",
        "country": "USA"
    }


@pytest.fixture
def employee_json_data() -> dict[str, Any]:
    return {
      "full_name": "John Doe",
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
      "company_id": "2"
    }


@pytest.fixture
def user_json_data() -> dict[str, Any]:
    return {
        "username": "User",
        "email": "user@example.com",
        "password": "Pa$word12!"
    }
