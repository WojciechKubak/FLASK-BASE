from app.service.repository.repository import EmployeeRepository


def test_find_all(employee_repository: EmployeeRepository) -> None:
    result = employee_repository.find_all()
    assert len(employee_repository.employees) == len(result)
