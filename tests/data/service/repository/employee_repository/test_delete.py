from app.service.repository.repository import EmployeeRepository


def test_when_id_is_present_in_data(employee_repository: EmployeeRepository) -> None:
    employee_repository.delete(0)
    assert 0 == len([e for e in employee_repository.employees if e.id_ == 2])
