from app.service.service.employee import EmployeeService


def test_get_employees_with_highest_and_lowest_salary(employee_service: EmployeeService) -> None:
    max_employee, min_employee = employee_service.get_employees_with_highest_and_lowest_salary()
    salaries = [employee.salary for employee in employee_service.find_all()]
    assert max(salaries) == max_employee.salary
    assert min(salaries) == min_employee.salary
