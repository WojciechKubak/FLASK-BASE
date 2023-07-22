from app.service.service.employee import EmployeeService


def test_find_all(employee_service: EmployeeService) -> None:
    result = employee_service.find_all()
    assert employee_service.employee_repository.employees == result
