from app.model.company import CompanyModel
from app.data.validator import CompanyJsonValidator
from dataclasses import dataclass
from typing import Any, ClassVar
import json
import os


@dataclass
class CompanyService:
    """
    Service class for managing company-related operations.

    Attributes:
        COMPANY_NOT_FOUND_ERROR_MSG (ClassVar[str]): Error message for when a company is not found.
    """

    COMPANY_NOT_FOUND_ERROR_MSG: ClassVar[str] = 'Company not found'

    def __post_init__(self):
        _company_constraints = json.loads(os.environ.get('COMPANY_CONSTRAINTS'))
        self.company_validator = CompanyJsonValidator(**_company_constraints)

    def add_company(self, data: dict[str, Any]) -> CompanyModel:
        """
        Adds a new company to the database.

        Args:
            data (dict[str, Any]): Company data to be added.

        Returns:
            CompanyModel: The newly added company.

        Raises:
            ValueError: If the company with the same name already exists or data validation fails.
        """
        if CompanyModel.find_by_name(data['name']):
            raise ValueError('Company already exists')

        self.company_validator.validate(data)
        company = CompanyModel(**data)
        company.add()

        return company

    def update_company(self, data: dict[str, Any]) -> CompanyModel:
        """
        Updates an existing company in the database.

        Args:
            data (dict[str, Any]): Updated company data.

        Returns:
            CompanyModel: The updated company.

        Raises:
            ValueError: If the company is not found or data validation fails.
        """
        if not (company := CompanyModel.find_by_name(data['name'])):
            raise ValueError(self.COMPANY_NOT_FOUND_ERROR_MSG)
        
        self.company_validator.validate(data)
        company.update(data)
        return company

    def delete_company(self, name: str) -> int:
        """
        Deletes a company from the database by its name.

        Args:
            name (str): The name of the company to be deleted.

        Returns:
            int: The ID of the deleted company.

        Raises:
            ValueError: If the company is not found.
        """
        if not (company := CompanyModel.find_by_name(name)):
            raise ValueError(self.COMPANY_NOT_FOUND_ERROR_MSG)
        company.delete()
        return company.id

    def get_company_by_name(self, name: str) -> CompanyModel:
        """
        Retrieves a company from the database by its name.

        Args:
            name (str): The name of the company to retrieve.

        Returns:
            CompanyModel: The retrieved company.

        Raises:
            ValueError: If the company is not found.
        """
        if not (company := CompanyModel.find_by_name(name)):
            raise ValueError(self.COMPANY_NOT_FOUND_ERROR_MSG)
        return company

    def get_all_companies(self) -> list[CompanyModel]:
        """
        Retrieves a list of all companies in the database.

        Returns:
            list[CompanyModel]: A list of CompanyModel objects representing all companies.
        """
        return CompanyModel.query.all()

    def add_or_update_many(self, data: list[dict[str, Any]]) -> list[CompanyModel]:
        """
        Adds or updates multiple companies based on the provided data.

        Args:
            data (list[dict[str, Any]]): A list of company data to be added or updated.

        Returns:
            list[CompanyModel]: A list of CompanyModel objects representing the added or updated companies.
        """
        return [self.update_company(record) if CompanyModel.find_by_name(record['name'])
                else self.add_company(record) for record in data]
