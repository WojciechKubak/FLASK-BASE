from app.data.model.company import Company
from app.data.model.employee import Employee
from typing import Any


class TestCompanyFromDict:

    def test_when_data_has_no_employee(self, company_record_data: dict[str, Any]) -> None:
        result = Company.from_dict(company_record_data)
        assert isinstance(result.id_, int)
        assert not result.employees

    def test_when_data_has_employee_ids(self, company_record_data: dict[str, Any]) -> None:
        company_record_data['employees'] = [1, 2, 3]
        result = Company.from_dict(company_record_data)
        assert 3 == len(result.employees)

    def test_when_data_has_employee_objects(
            self,
            company_record_data: dict[str, Any],
            employee_obj_mock: Employee) -> None:
        company_record_data['employees'] = [employee_obj_mock, employee_obj_mock]
        result = Company.from_dict(company_record_data)
        assert 2 == len(result.employees)
