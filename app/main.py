from app.data.factory.factory import DataFactoryType
from app.data.factory.processor import DataProcessor
from typing import Final


def call_employee_processor() -> None:
    EMPLOYEE_DATA_PATH: Final[str] = '../resources/employees/employees_data_1.json'
    employee_constraints = {
        'first_name_regex': r'^[A-Z][a-z]+$',
        'last_name_regex': r'^[A-Z][a-z]+$',
        'position_regex': r'^([A-Z][a-z]+)+(?: ([A-Z][a-z]+)+)*$',
        'department_regex': r'([A-Za-z\s&]+)',
    }
    employee_processor = DataProcessor.create_processor(
        DataFactoryType.EMPLOYEE_FACTORY,
        EMPLOYEE_DATA_PATH,
        employee_constraints
    )
    print(employee_processor.process())


def call_company_processor() -> None:
    COMPANY_DATA_PATH: Final[str] = '../resources/companies/companies_data_1.json'
    company_constraints = {
        'company_name_regex': r'^[a-zA-Z0-9 .]+$',
        'street_regex': r'^[1-9][0-9]{2} [A-Z][a-z]+(?: [A-Z][a-z]+)*$',
        'city_regex': r'^([A-Z][a-z]+)+(?: ([A-Z][a-z]+)+)*$',
        'state_regex': r'^[A-Z]+$',
        'country_regex': r'^[A-Za-z]+(?: [A-Za-z]+)*$',
    }
    company_processor = DataProcessor.create_processor(
        DataFactoryType.COMPANY_FACTORY,
        COMPANY_DATA_PATH,
        company_constraints
    )
    print(company_processor.process())


if __name__ == '__main__':
    call_employee_processor()
    call_company_processor()
