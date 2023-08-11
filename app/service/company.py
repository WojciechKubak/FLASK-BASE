from app.model.company import CompanyModel
from dataclasses import dataclass
from typing import Any, ClassVar


@dataclass(frozen=True, order=True)
class CompanyService:
    COMPANY_NOT_FOUND_ERROR_MSG: ClassVar[str] = 'Company not found'

    def add_company(self, data: dict[str, Any]) -> None:
        if CompanyModel.find_by_name(data['company_name']):
            raise ValueError('Company already exists')
        company = CompanyModel(**data)
        company.add()

    def update_company(self, data: dict[str, Any]) -> None:
        if not (company := CompanyModel.find_by_name(data['company_name'])):
            raise ValueError(CompanyService.COMPANY_NOT_FOUND_ERROR_MSG)
        company.update(data)

    def delete_company(self, name: str) -> None:
        if not (company := CompanyModel.find_by_name(name)):
            raise ValueError(CompanyService.COMPANY_NOT_FOUND_ERROR_MSG)
        company.delete()

    def get_company_by_name(self, name: str) -> CompanyModel:
        if not (company := CompanyModel.find_by_name(name)):
            raise ValueError(CompanyService.COMPANY_NOT_FOUND_ERROR_MSG)
        return company

    def get_all_companies(self) -> list[CompanyModel]:
        return CompanyModel.query.all()

    def add_or_update_many(self, data: list[dict[str, Any]]) -> None:
        for record in data:
            if result := CompanyModel.find_by_name(record['company_name']):
                result.update(record)
            else:
                CompanyModel(**record).add()
