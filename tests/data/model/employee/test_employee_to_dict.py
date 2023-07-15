from app.data.model.employee import Employee
from app.data.model.company import Company
from typing import Any


class TestEmployeeToDict:

    def test_when_converted_correctly(self, employee_record_test: dict[str, Any]) -> None:
        employee = Employee.from_dict(employee_record_test)
        result = employee.to_dict()
        assert len(employee_record_test) == len(result)
        assert 'id' in result

    def test_when_company_id_in_employee_obj(self, employee_class_obj_with_company_id: Employee) -> None:
        result = employee_class_obj_with_company_id.to_dict()
        assert 2 == result['company']

    def test_when_company_data_in_employee_obj(self, employee_class_obj_with_company_obj: Employee) -> None:
        result = employee_class_obj_with_company_obj.to_dict()
        assert isinstance(result['company'], Company)
