from app.service.additional.exporter import DataExporter, FileExportFormat
from app.data.model.employee import Employee
from pathlib import Path
import pytest
import json
import os


@pytest.fixture
def export_json_path(tmp_path: Path) -> str:
    return os.path.join(tmp_path, 'result.json')


class TestExportToJson:

    def test_when_path_contains_incorrect_extension(self, export_json_path: str) -> None:
        with pytest.raises(AttributeError) as err:
            DataExporter().export([], f'{export_json_path}nn', FileExportFormat.JSON_FILE)
        assert 'Incorrect file extension.' == str(err.value)

    def test_when_path_does_not_exist(self, export_json_path: str) -> None:
        with pytest.raises(FileNotFoundError) as err:
            DataExporter().export([], f'directory/{export_json_path}', FileExportFormat.JSON_FILE)
        assert str(err.value).startswith('Error occurred')

    def test_when_export_to_json_works_correctly(self, employee_obj: Employee, export_json_path: str) -> None:
        data = [employee_obj, employee_obj]
        DataExporter().export(data, export_json_path, FileExportFormat.JSON_FILE)
        with open(export_json_path, 'r', encoding='utf-8') as json_data:
            result = json.load(json_data)
        assert len(data) == len(result)
        assert employee_obj.id_ == result[0]['id']
        assert employee_obj.company == result[0]['company']
