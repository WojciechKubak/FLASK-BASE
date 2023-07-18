from app.data.model.employee import Employee
from typing import Callable, Any
import pytest


class TestEmployeeFilterByCriterion:

    def test_when_attribute_is_not_correct(self, employee_obj: Employee) -> None:
        with pytest.raises(AttributeError) as err:
            employee_obj.filter_by_criterion(('not existing attr', lambda x: True))
        assert 'Key not found.' == str(err.value)

    @pytest.mark.parametrize(
        'test_input,expected', [
            (('age', lambda x: 21 < x < 35), True),
            (('position', lambda x: x.lower().endswith('developer')), True),
            (('company', lambda x: x == 4), False)
        ]
    )
    def test_when_attribute_is_correct(
            self,
            test_input: tuple[str, Callable[[Any], bool]],
            expected: bool,
            employee_obj: Employee
    ) -> None:
        assert expected == employee_obj.filter_by_criterion(test_input)
