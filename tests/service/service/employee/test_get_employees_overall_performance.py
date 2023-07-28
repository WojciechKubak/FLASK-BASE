from app.service.service.employee import EmployeeService


def test_get_employees_overall_performance(employee_service: EmployeeService) -> None:
    result = employee_service.get_employees_overall_performance()
    expected = employee_service.find_all()
    assert len(expected) == len(result)
    for employee in expected:
        assert employee.id_ in result
        expected_score = sum(employee.performance_rating.values()) / len(employee.performance_rating)
        assert expected_score == result[employee.id_]
