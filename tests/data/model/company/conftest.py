from app.data.model.employee import Employee
from app.data.model.company import Company
from unittest.mock import MagicMock
import pytest


@pytest.fixture
def employee_obj_mock() -> Employee | MagicMock:
    employee_mock = MagicMock(spec=Employee)
    employee_mock.to_dict.return_value = {}
    employee_mock.__str__.return_value = 'employee data'
    return employee_mock


@pytest.fixture
def company_with_no_employees_data(company_record_data) -> Company:
    return Company.from_dict(company_record_data)


@pytest.fixture
def company_with_employee_objects(company_record_data, employee_obj_mock: Employee) -> Company:
    company_record_data['employees'] = [employee_obj_mock, employee_obj_mock]
    return Company.from_dict(company_record_data)


@pytest.fixture
def company_with_employee_ids(company_record_data) -> Company:
    company_record_data['employees'] = [2, 3, 4]
    return Company.from_dict(company_record_data)
