from app.service.service.employee import EmployeeService


def test_get_employees_salary_average_mean(employee_service: EmployeeService) -> None:
    result = employee_service.get_employees_salary_average_mean()
    all_salaries = [employee.salary for employee in employee_service.find_all()]
    expected_mean_salary = sum(all_salaries) / len(all_salaries)
    assert expected_mean_salary == result
