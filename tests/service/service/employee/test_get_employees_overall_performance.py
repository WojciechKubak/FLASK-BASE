from app.service.service.employee import EmployeeService


def test_get_employees_overall_performance(employee_service: EmployeeService) -> None:
    result = employee_service.get_employees_overall_performance()

    assert len(result) == len(employee_service.find_all())

    for employee in employee_service.find_all():
        assert employee.id_ in result

    for employee in employee_service.find_all():
        expected_score = sum(employee.performance_rating.values()) / len(employee.performance_rating)
        assert expected_score == result[employee.id_]
