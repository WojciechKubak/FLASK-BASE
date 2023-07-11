from typing import Any
from unittest.mock import patch, PropertyMock
from app.data.organization.employee import Employee
import pytest


def test_employee_get_performance_average_works_correctly(employee_record_test: dict[str, Any]) -> None:
    # todo: (1)
    """
    1. jaki powinen przyjąć standard co do pola performance_rating w klasie Employee, żeby później nie było z tym problemu?
    2. jak miałyby wyglądać testy metody employee.get_performance_average()? (frozenInstance)
    """
    # employee_obj = Employee.from_dict(employee_record_test)
    # with patch.object(employee_obj, 'performance_rating', new_callable=PropertyMock) as attr_mock:
    #     attr_mock.return_value = {'x': 1, 'y': 2, 'z': 3}
    #     assert 2.0 == employee_obj.get_performance_average()
    ...
