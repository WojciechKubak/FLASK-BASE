from app.service.service.employee import EmployeeService


def test_get_department_employee_salary_overview(employee_service: EmployeeService) -> None:
    result = employee_service.get_department_employee_salary_overview()

    for department, salary in result.items():
        employees_in_department = [e for e in employee_service.find_all() if e.department == department]
        total_salary = sum(employee.salary for employee in employees_in_department)
        expected_salary = total_salary / len(employees_in_department)
        assert expected_salary == salary
