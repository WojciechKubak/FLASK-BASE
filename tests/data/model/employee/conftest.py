from app.data.model.employee import Employee
from app.data.model.company import Company
from unittest.mock import MagicMock
from typing import Any
import pytest


@pytest.fixture
def employee_class_obj_with_company_id(employee_record_test: dict[str, Any]) -> Employee:
    return Employee.from_dict(employee_record_test)


@pytest.fixture
def employee_class_obj_with_company_obj(employee_record_test: dict[str, Any]) -> Employee:
    company_mock = MagicMock(spec=Company)
    company_mock.__str__.return_value = 'Example company data text'
    employee_record_test['company'] = company_mock
    return Employee.from_dict(employee_record_test)
