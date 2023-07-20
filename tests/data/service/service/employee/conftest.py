from app.service.repository.repository import EmployeeRepository
from app.service.service.employee import EmployeeService
from typing import Any
import pytest


@pytest.fixture
def employee_repository(employee_test_path: str, employee_validator_constraints: dict[str, Any]) -> EmployeeRepository:
    return EmployeeRepository(employee_test_path, employee_validator_constraints)


@pytest.fixture
def employee_service(employee_repository: EmployeeRepository) -> EmployeeService:
    return EmployeeService(employee_repository)
