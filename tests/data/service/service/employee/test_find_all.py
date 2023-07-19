from app.service.service.employee import EmployeeService


def test_find_all(employee_service: EmployeeService) -> None:
    result = employee_service.find_all()
    assert 2 == len(result)
    assert result[0].id_ == 0
    assert result[1].id_ == 1
