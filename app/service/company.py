from app.model.company import CompanyModel
from app.data.validator import CompanyJsonValidator
from dataclasses import dataclass
from typing import Any, ClassVar
import json
import os


@dataclass
class CompanyService:
    COMPANY_NOT_FOUND_ERROR_MSG: ClassVar[str] = 'Company not found'

    def __post_init__(self):
        _company_constraints = json.loads(os.environ.get('COMPANY_CONSTRAINTS'))
        self.company_validator = CompanyJsonValidator(**_company_constraints)

    def add_company(self, data: dict[str, Any]) -> CompanyModel:
        if CompanyModel.find_by_name(data['name']):
            raise ValueError('Company already exists')

        self.company_validator.validate(data)
        company = CompanyModel(**data)
        company.add()

        return company

    def update_company(self, data: dict[str, Any]) -> CompanyModel:
        if not (company := CompanyModel.find_by_name(data['name'])):
            raise ValueError(self.COMPANY_NOT_FOUND_ERROR_MSG)
        
        self.company_validator.validate(data)
        company.update(data)
        return company

    def delete_company(self, name: str) -> None:
        if not (company := CompanyModel.find_by_name(name)):
            raise ValueError(self.COMPANY_NOT_FOUND_ERROR_MSG)
        company.delete()

    def get_company_by_name(self, name: str) -> CompanyModel:
        if not (company := CompanyModel.find_by_name(name)):
            raise ValueError(self.COMPANY_NOT_FOUND_ERROR_MSG)
        return company

    def get_all_companies(self) -> list[CompanyModel]:
        return CompanyModel.query.all()

    def add_or_update_many(self, data: list[dict[str, Any]]) -> list[CompanyModel]:
        return [self.update_company(record) if CompanyModel.find_by_name(record['name'])
                else self.add_company(record) for record in data]
