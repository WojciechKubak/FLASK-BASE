from app.data.model.employee import Employee
from app.data.factory.factory import \
    FromJsonWithValidationToEmployeeDataFactory, FromJsonWithValidationToCompanyDataFactory
from app.data.layers.validator import CompanyJsonValidator, EmployeeJsonValidator
from app.service.repository.repository import CompanyRepository, EmployeeRepository, ProxyCompanyRepository
from app.service.service.company import CompanyService
from app.service.service.employee import EmployeeService
from typing import Any
from pathlib import Path
import pytest
import os


@pytest.fixture
def company_test_path() -> str:
    return 'tests/example_data/companies'


@pytest.fixture
def employee_test_path() -> str:
    return 'tests/example_data/employees'


@pytest.fixture
def empty_directory_path() -> str:
    return 'tests/example_data/empty_directory'


@pytest.fixture
def company_record_data() -> dict[str, Any]:
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
def employee_record_data() -> dict[str, Any]:
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
def employee_obj(employee_record_data: dict[str, Any]) -> Employee:
    return Employee.from_dict(employee_record_data)


@pytest.fixture
def employee_obj_with_expected_id(request: Any, employee_record_data: dict[str, Any]) -> Employee:
    employee_record_data['id'] = request.param
    return Employee.from_dict(employee_record_data)


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


@pytest.fixture
def export_json_path(tmp_path: Path) -> str:
    return os.path.join(tmp_path, 'result.json')


@pytest.fixture
def export_txt_path(tmp_path: Path) -> str:
    return os.path.join(tmp_path, 'result.txt')


@pytest.fixture
def employee_repository(employee_test_path: str, employee_validator_constraints: dict[str, Any]) -> EmployeeRepository:
    return EmployeeRepository(employee_test_path, employee_validator_constraints)


@pytest.fixture
def employee_service(employee_repository: EmployeeRepository) -> EmployeeService:
    return EmployeeService(employee_repository)


@pytest.fixture
def company_repository(company_test_path: str, company_validator_constraints: dict[str, Any]) -> CompanyRepository:
    return CompanyRepository(company_test_path, company_validator_constraints)


@pytest.fixture
def company_service(company_repository: CompanyRepository) -> CompanyService:
    return CompanyService(company_repository)
