from app.service.service.employee import EmployeeService
from typing import Callable, Any
import pytest


class TestFilterBy:

    def test_when_attribute_is_not_present(self, employee_service: EmployeeService) -> None:
        with pytest.raises(AttributeError) as err:
            employee_service.filter_by(('un-existing key', lambda x: True))
        assert 'Key not found.' == str(err.value)

    @pytest.mark.parametrize('test_input,expected', [
        (('first_name', lambda x: x == 'Jane'), 1),
        (('age', lambda x: 21 <= x <= 30), 0),
        (('position', lambda x: 'manager' in x.lower()), 3),
        (('company', lambda x: x < 3), 4)
        ]
    )
    def test_when_attribute_is_correct(
            self,
            employee_service: EmployeeService,
            test_input: tuple[str, Callable[[Any], bool]],
            expected: int
    ) -> None:
        assert expected == len(employee_service.filter_by(test_input))
