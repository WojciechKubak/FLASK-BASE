from app.service.repository.repository import EmployeeRepository, CompanyRepository, ProxyCompanyRepository, FetchType
from app.service.service.employee import EmployeeService
from app.service.service.company import CompanyService
from app.service.additional.exporter import FileExportFormat


"""
    1. testy dla CRUD repozytoriów,
    2. testy dla Exportera,
    3. testy dla metody serwisowej do eksportowania,
    4. refaktoryzacja testów z Chatem.
"""


def call_employee_repository() -> EmployeeRepository:
    employee_data_dir = '../resources/employees/'
    employee_constraints = {
        'first_name_regex': r'^[A-Z][a-z]+$',
        'last_name_regex': r'^[A-Z][a-z]+$',
        'position_regex': r'^([A-Z][a-z]+)+(?: ([A-Z][a-z]+)+)*$',
        'department_regex': r'([A-Za-z\s&]+)',
    }
    return EmployeeRepository(employee_data_dir, employee_constraints)


def call_company_repository() -> CompanyRepository:
    company_data_dir = '../resources/companies'
    company_constraints = {
        'company_name_regex': r'^[a-zA-Z0-9 .]+$',
        'street_regex': r'^[1-9][0-9]{2} [A-Z][a-z]+(?: [A-Z][a-z]+)*$',
        'city_regex': r'^([A-Z][a-z]+)+(?: ([A-Z][a-z]+)+)*$',
        'state_regex': r'^[A-Z]+$',
        'country_regex': r'^[A-Za-z]+(?: [A-Za-z]+)*$',
    }
    return CompanyRepository(company_data_dir, company_constraints)


if __name__ == '__main__':
    employee_repository = call_employee_repository()
    company_repository = call_company_repository()

    company_repository_lazy = ProxyCompanyRepository(company_repository, employee_repository, FetchType.LAZY)
    company_repository_eager = ProxyCompanyRepository(company_repository, employee_repository, FetchType.EAGER)

    employee_service = EmployeeService(employee_repository)
    company_service_lazy = CompanyService(company_repository_lazy)
    company_service_eager = CompanyService(company_repository_eager)

    company_service_eager.export_data('../results/company_data.json', FileExportFormat.JSON_FILE)
    company_service_eager.export_data('../results/company_data.txt', FileExportFormat.TXT_FILE)
    employee_service.export_data('../results/employee_data.json', FileExportFormat.JSON_FILE)
    employee_service.export_data('../results/employee_data.txt', FileExportFormat.TXT_FILE)
