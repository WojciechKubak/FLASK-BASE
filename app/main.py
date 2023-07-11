from app.service.additionals.repository import Repository
from app.service.employees import \
    FetchType, EmployeeRepository, ProxyEmployeeRepository, EmployeeService
from app.service.companies import CompanyRepository, CompanyService
from typing import Final


def call_employee_repository() -> Repository:
    EMPLOYEE_DATA_PATH: Final[str] = '../resources/employees/employees_data_1.json'
    employee_constraints = {
        'first_name_regex': r'^[A-Z][a-z]+$',
        'last_name_regex': r'^[A-Z][a-z]+$',
        'position_regex': r'^([A-Z][a-z]+)+(?: ([A-Z][a-z]+)+)*$',
        'department_regex': r'([A-Za-z\s&]+)',
    }
    return EmployeeRepository(EMPLOYEE_DATA_PATH, employee_constraints)


def call_company_repository() -> Repository:
    COMPANY_DATA_PATH: Final[str] = '../resources/companies/companies_data_1.json'
    company_constraints = {
        'company_name_regex': r'^[a-zA-Z0-9 .]+$',
        'street_regex': r'^[1-9][0-9]{2} [A-Z][a-z]+(?: [A-Z][a-z]+)*$',
        'city_regex': r'^([A-Z][a-z]+)+(?: ([A-Z][a-z]+)+)*$',
        'state_regex': r'^[A-Z]+$',
        'country_regex': r'^[A-Za-z]+(?: [A-Za-z]+)*$',
    }
    return CompanyRepository(COMPANY_DATA_PATH, company_constraints)


if __name__ == '__main__':
    employee_repository = call_employee_repository()
    company_repository = call_company_repository()

    employee_proxy_repo_lazy = ProxyEmployeeRepository(employee_repository, company_repository, FetchType.LAZY)
    employee_proxy_repo_eager = ProxyEmployeeRepository(employee_repository, company_repository, FetchType.EAGER)


