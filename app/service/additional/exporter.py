from dataclasses import dataclass
from typing import Any, ClassVar
import csv
import json


@dataclass(frozen=True, order=True)
class DataExporter:
    ENCODING: ClassVar[str] = 'utf-8'
    ATTRIBUTE_ERROR_MSG: ClassVar[str] = 'Incorrect file extension.'

    @staticmethod
    def export_to_csv(data: list[dict[str, Any]], path: str) -> None:
        if not path.endswith('.csv'):
            raise AttributeError(DataExporter.ATTRIBUTE_ERROR_MSG)
        try:
            with open(path, 'w', encoding=DataExporter.ENCODING) as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=data[0].values())
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            raise FileNotFoundError(f'Error occurred: {e.args[0]}.')

    @staticmethod
    def export_to_txt(data: list[Any], path: str, sep: str = ',') -> None:
        if not path.endswith('.txt'):
            raise AttributeError(DataExporter.ATTRIBUTE_ERROR_MSG)
        try:
            with open(path, 'w', encoding=DataExporter.ENCODING) as txt_file:
                txt_file.writelines([sep.join(record.values()) for record in data])
        except Exception as e:
            raise FileNotFoundError(f'Error occurred: {e.args[0]}.')

    @staticmethod
    def export_to_json(data: list[Any], path: str) -> None:
        if not path.endswith('.csv'):
            raise AttributeError(DataExporter.ATTRIBUTE_ERROR_MSG)
        try:
            with open(path, 'w', encoding=DataExporter.ENCODING) as json_file:
                json.dump(data, json_file)
        except Exception as e:
            raise FileNotFoundError(f'Error occurred: {e.args[0]}.')
