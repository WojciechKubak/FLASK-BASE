from app.data.model.employee import Employee
from app.data.model.company import Company
from decimal import Decimal
from typing import Any
from unittest.mock import MagicMock


class TestEmployeeClassFromDict:

    def test_basic_type_conversion(self, employee_record_test: dict[str, Any]) -> None:
        result = Employee.from_dict(employee_record_test)
        assert isinstance(result, Employee)
        assert 0 == result.id_
        assert 32 == result.age
        assert Decimal('7000') == result.salary

    def test_when_data_contains_company_id(self, employee_record_test: dict[str, Any]) -> None:
        result = Employee.from_dict(employee_record_test)
        assert 2 == result.company

    def test_when_data_contains_company_obj(self, employee_record_test: dict[str, Any]) -> None:
        company_mock = MagicMock(spec=Company)
        employee_record_test['company'] = company_mock
        result = Employee.from_dict(employee_record_test)
        assert isinstance(result.company, Company)
