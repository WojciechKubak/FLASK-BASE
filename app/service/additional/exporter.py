from dataclasses import dataclass
from typing import Any, ClassVar
from enum import Enum, auto
import json


class FileExportFormat(Enum):
    """
    Enumeration of file export formats.

    Attributes:
        TXT_FILE (FileExportFormat): Represents the TXT file export format.
        JSON_FILE (FileExportFormat): Represents the JSON file export format.
    """
    TXT_FILE = auto()
    JSON_FILE = auto()


@dataclass(frozen=True, order=True)
class DataExporter:
    """
    DataExporter class for exporting data to different file formats.

    Class Variables:
        ENCODING (ClassVar[str]): The encoding to be used for writing the files (default is 'utf-8').
        ATTRIBUTE_ERROR_MSG (ClassVar[str]): The error message for incorrect file extension.
    """

    ENCODING: ClassVar[str] = 'utf-8'
    ATTRIBUTE_ERROR_MSG: ClassVar[str] = 'Incorrect file extension.'

    def export(self, data: list[Any], path: str, export_format: FileExportFormat) -> None:
        """
        Export the data to the specified file format.

        Args:
            data (list[Any]): The list of data objects to export.
            path (str): The path to the output file.
            export_format (FileExportFormat): The file export format to use.

        Raises:
            AttributeError: If the file extension is incorrect.
        """
        if export_format == FileExportFormat.JSON_FILE:
            self._export_to_json(data, path)
        elif export_format == FileExportFormat.TXT_FILE:
            self._export_to_txt(data, path)

    @staticmethod
    def _export_to_txt(data: list[Any], path: str, sep: str = ';') -> None:
        """
        Export the data to a TXT file format with a specified separator.

        Args:
            data (list[Any]): The list of data objects to export.
            path (str): The path to the output TXT file.
            sep (str): The separator used for separating data attributes in the TXT file (default is ';').

        Raises:
            AttributeError: If the file extension is incorrect.
            FileNotFoundError: If an error occurs while exporting the data.
        """
        if not path.endswith('.txt'):
            raise AttributeError(DataExporter.ATTRIBUTE_ERROR_MSG)
        try:
            with open(path, 'w', encoding=DataExporter.ENCODING) as txt_file:
                txt_file.writelines([record.__str__().replace('\n', sep) + '\n' for record in data])
        except Exception as e:
            raise FileNotFoundError(f'Error occurred: {e.args[0]}.')

    @staticmethod
    def _export_to_json(data: list[Any], path: str) -> None:
        """
        Export the data to a JSON file format.

        Args:
            data (list[Any]): The list of data objects to export.
            path (str): The path to the output JSON file.

        Raises:
            AttributeError: If the file extension is incorrect.
            FileNotFoundError: If an error occurs while exporting the data.
        """
        if not path.endswith('.json'):
            raise AttributeError(DataExporter.ATTRIBUTE_ERROR_MSG)
        try:
            with open(path, 'w', encoding=DataExporter.ENCODING) as json_file:
                json.dump([record.to_dict() for record in data], json_file, default=str, indent=4)
        except Exception as e:
            raise FileNotFoundError(f'Error occurred: {e.args[0]}.')
