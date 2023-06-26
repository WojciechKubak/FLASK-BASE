from app.data.factory.factory import \
    FromJsonWithValidationToEmployeeDataFactory, FromJsonWithValidationToCompanyDataFactory
from app.data.layers.validator import CompanyJsonValidator, EmployeeJsonValidator
import pytest


@pytest.fixture
def company_test_path():
    return 'tests/example_data/company_data_test.json'


@pytest.fixture
def employee_test_path():
    return 'tests/example_data/employee_data_test.json'


@pytest.fixture
def company_empty_test_path():
    return 'tests/example_data/company_data_empty_test.json'


@pytest.fixture
def employee_empty_test_path():
    return 'tests/example_data/employee_data_empty_test'


@pytest.fixture
def company_record_test():
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
def employee_record_test():
    return {
      "id": "0",
      "first_name": "John",
      "last_name": "Doe",
      "position": "Senior Developer",
      "age": "32",
      "employment_tenure": "5",
      "salary": "7000",
      "performance_rating": {
         "efficiency": 4,
         "creativity": 5,
         "communication": 4
      },
      "company_id": "2"
    }


@pytest.fixture
def company_validator_constraints():
    return {
        'company_name_regex': r'^[a-zA-Z0-9 .]+$',
        'street_regex': r'^[1-9][0-9]{2} [A-Z][a-z]+(?: [A-Z][a-z]+)*$',
        'city_regex': r'^([A-Z][a-z]+)+(?: ([A-Z][a-z]+)+)*$',
        'state_regex': r'^[A-Z]+$',
        'country_regex': r'^[A-Za-z]+(?: [A-Za-z]+)*$',
    }


@pytest.fixture
def employee_validator_constraints():
    return {
        'first_name_regex': r'^[A-Z][a-z]+$',
        'last_name_regex': r'^[A-Z][a-z]+$',
        'position_regex': r'^([A-Z][a-z]+)+(?: ([A-Z][a-z]+)+)*$',
    }


@pytest.fixture
def company_validator_obj(company_validator_constraints):
    return CompanyJsonValidator(**company_validator_constraints)


@pytest.fixture
def employee_validator_obj(employee_validator_constraints):
    return EmployeeJsonValidator(**employee_validator_constraints)


@pytest.fixture
def company_data_factory(company_test_path, company_validator_constraints):
    return FromJsonWithValidationToCompanyDataFactory(company_test_path, company_validator_constraints)


@pytest.fixture
def employee_data_factory(employee_validator_constraints, employee_test_path):
    return FromJsonWithValidationToEmployeeDataFactory(employee_test_path, employee_validator_constraints)
