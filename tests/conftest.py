from app.config import TestingConfig
from app.db.configuration import sa
from flask import Flask
from typing import Any
import pytest
import json


@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)

    app.config.from_object(TestingConfig)
    sa.init_app(app)

    with app.app_context():
        sa.create_all()

    yield app

    with app.app_context():
        sa.drop_all()


@pytest.fixture()
def company_model_data() -> dict[str, Any]:
    return {
        'name': 'Company XYZ',
        'street': '123 Main Street',
        'city': 'Anytown',
        'postal_code': '54321',
        'state': 'CA',
        'country': 'USA'
    }


@pytest.fixture
def employee_model_data() -> dict[str, Any]:
    return {
        'full_name': 'John Smith',
        'position': 'Employee',
        'age': 30,
        'employment_tenure': 2,
        'department': 'Department A',
        'salary': 5000,
        'performance_rating': {
            'efficiency': 3,
            'creativity': 3,
            'communication': 3
        },
        'company_id': 1
    }


@pytest.fixture
def user_model_data() -> dict[str, str]:
    return {
        'username': 'TestUser',
        'email': 'user@example.com',
        'password': 'Password123!',
    }


@pytest.fixture
def employees_data_path() -> str:
    return 'tests/samples/employees.json'


@pytest.fixture
def companies_data_path() -> str:
    return 'tests/samples/companies.json'


@pytest.fixture
def company_records(companies_data_path: str) -> list[dict[str, Any]]:
    with open(companies_data_path, 'r', encoding='utf-8') as json_data:
        return json.load(json_data, parse_int=int, parse_float=float)


@pytest.fixture
def employee_records(employees_data_path: str) -> list[dict[str, Any]]:
    with open(employees_data_path, 'r', encoding='utf-8') as json_data:
        return json.load(json_data, parse_int=int, parse_float=float)
