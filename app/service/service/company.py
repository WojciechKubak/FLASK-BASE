from app.service.repository.repository import Repository
from app.service.additional.exporter import DataExporter, FileExportFormat
from dataclasses import dataclass
from typing import Any


@dataclass
class CompanyService:
    """
    Service class for managing Company data and exporting it to different formats.

    Attributes:
        company_repository (Repository): The repository instance for Company data.
    """

    company_repository: Repository

    def find_all(self) -> list[Any]:
        """
        Retrieve all Company records from the repository.

        Returns:
            list[Any]: A list of all Company records in the repository.
        """
        return self.company_repository.find_all()

    def find_by_id(self, id_: int) -> Any:
        """
        Retrieve a Company record from the repository based on its ID.

        Args:
            id_ (int): The ID of the Company record to retrieve.

        Returns:
            Any: The Company record if found, otherwise None.
        """
        if id_ < 0:
            raise ValueError('Id must be non-negative number.')
        return self.company_repository.find_by_id(id_)

    def add_or_update(self, record: Any) -> None:
        """
        Add or update a Company record in the repository.

        Args:
            record (Any): The Company record to add or update.
        """
        self.company_repository.add_or_update(record)

    def delete(self, id_: int) -> None:
        """
        Delete a Company record from the repository based on its ID.

        Args:
            id_ (int): The ID of the Company record to delete.
        """
        if id_ < 0:
            raise ValueError('Id must be non-negative number.')
        self.company_repository.delete(id_)

    def export_data(self, path: str, export_type: FileExportFormat) -> None:
        """
        Export Company data to a specified file path in the desired export format.

        Args:
            path (str): The file path for exporting the data.
            export_type (FileExportFormat): The export format (TXT_FILE or JSON_FILE).
        """
        DataExporter().export(self.find_all(), path, export_type)
