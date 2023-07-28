from app.service.service.employee import EmployeeService


def test_get_employees_with_highest_and_lowest_salary(employee_service: EmployeeService) -> None:
    result = employee_service.get_employees_with_highest_and_lowest_salary()
    max_employees, min_employees = result['max'], result['min']
    salaries = [employee.salary for employee in employee_service.find_all()]

    expected_max_salary = max(salaries)
    for employee in max_employees:
        assert expected_max_salary == employee.salary

    expected_min_salary = min(salaries)
    for employee in min_employees:
        assert expected_min_salary == employee.salary
