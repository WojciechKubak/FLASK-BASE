from app.service.repository.repository import EmployeeRepository


def test_find_by_id(employee_repository: EmployeeRepository) -> None:
    result = employee_repository.find_by_id(0)
    assert result in employee_repository.employees
