from app.service.service.employee import EmployeeService


def test_find_all(employee_service: EmployeeService) -> None:
    result = employee_service.find_all()
    assert 4 == len(result)
    assert 0 == result[0].id_
    assert 1 == result[1].id_
