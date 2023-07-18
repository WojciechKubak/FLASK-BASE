from dataclasses import dataclass
from typing import Any, ClassVar
from enum import Enum, auto
import json


class FileExportFormat(Enum):
    TXT_FILE = auto()
    JSON_FILE = auto()


@dataclass(frozen=True, order=True)
class DataExporter:
    ENCODING: ClassVar[str] = 'utf-8'
    ATTRIBUTE_ERROR_MSG: ClassVar[str] = 'Incorrect file extension.'

    def export(self, data: list[Any], path: str, export_format: FileExportFormat) -> None:
        if export_format == FileExportFormat.JSON_FILE:
            self._export_to_json(data, path)
        elif export_format == FileExportFormat.TXT_FILE:
            self._export_to_txt(data, path)

    @staticmethod
    def _export_to_txt(data: list[Any], path: str, sep: str = ';') -> None:
        if not path.endswith('.txt'):
            raise AttributeError(DataExporter.ATTRIBUTE_ERROR_MSG)
        try:
            with open(path, 'w', encoding=DataExporter.ENCODING) as txt_file:
                txt_file.writelines([record.__str__().replace('\n', sep) + '\n' for record in data])
        except Exception as e:
            raise FileNotFoundError(f'Error occurred: {e.args[0]}.')

    @staticmethod
    def _export_to_json(data: list[Any], path: str) -> None:
        if not path.endswith('.json'):
            raise AttributeError(DataExporter.ATTRIBUTE_ERROR_MSG)
        try:
            with open(path, 'w', encoding=DataExporter.ENCODING) as json_file:
                json.dump([record.to_dict() for record in data], json_file, default=str, indent=4)
        except Exception as e:
            raise FileNotFoundError(f'Error occurred: {e.args[0]}.')
