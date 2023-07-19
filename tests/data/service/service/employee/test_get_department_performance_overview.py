from app.service.service.employee import EmployeeService


def test_get_department_performance_overview(employee_service: EmployeeService) -> None:
    result = employee_service.get_department_performance_overview()

    unique_departments = set(e.department for e in employee_service.find_all())
    assert len(unique_departments) == len(result)

    for department, score in result.items():
        employees_in_department = [e for e in employee_service.find_all() if e.department == department]
        expected_score = sum(
            sum(employee.performance_rating.values()) / len(employee.performance_rating) for employee in
            employees_in_department) / len(employees_in_department)
        assert expected_score == score
