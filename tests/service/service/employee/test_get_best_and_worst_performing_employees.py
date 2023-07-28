from app.service.service.employee import EmployeeService


def test_get_best_and_worst_performing_employees(employee_service: EmployeeService) -> None:
    performance_overview = employee_service.get_best_and_worst_performing_employees()
    best_employees, worst_employees = performance_overview['max'], performance_overview['min']
    scores = [employee.get_performance_average() for employee in employee_service.find_all()]

    expected_best_score = max(scores)
    for employee in best_employees:
        assert expected_best_score == employee.get_performance_average()

    expected_worst_score = min(scores)
    for employee in worst_employees:
        assert expected_worst_score == employee.get_performance_average()
