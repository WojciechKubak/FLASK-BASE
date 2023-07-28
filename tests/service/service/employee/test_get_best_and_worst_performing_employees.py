from app.service.service.employee import EmployeeService


def test_get_best_and_worst_performing_employees(employee_service: EmployeeService) -> None:
    best_employee, worst_employee = employee_service.get_best_and_worst_performing_employees()

    expected_best_score = max(employee.get_performance_average() for employee in employee_service.find_all())
    assert expected_best_score == best_employee.get_performance_average()

    expected_worst_score = min(employee.get_performance_average() for employee in employee_service.find_all())
    assert expected_worst_score == worst_employee.get_performance_average()
