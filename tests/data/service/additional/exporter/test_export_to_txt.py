from app.service.additional.exporter import DataExporter, FileExportFormat
from app.data.model.employee import Employee
from pathlib import Path
import pytest
import os


@pytest.fixture
def export_txt_path(tmp_path: Path) -> str:
    return os.path.join(tmp_path, 'result.txt')


class TestExportToTxt:

    def test_when_path_contains_incorrect_extension(self, export_txt_path: str) -> None:
        with pytest.raises(AttributeError) as err:
            DataExporter().export([], f'{export_txt_path}tt', FileExportFormat.TXT_FILE)
        assert 'Incorrect file extension.' == str(err.value)

    def test_when_path_does_not_exist(self, export_txt_path: str) -> None:
        with pytest.raises(FileNotFoundError) as err:
            DataExporter().export([], f'directory/{export_txt_path}', FileExportFormat.TXT_FILE)
        assert str(err.value).startswith('Error occurred')

    def test_when_export_to_txt_works_correctly(self, employee_obj: Employee, export_txt_path: str) -> None:
        data = [employee_obj, employee_obj]
        DataExporter().export(data, export_txt_path, FileExportFormat.TXT_FILE)
        with open(export_txt_path, 'r', encoding='utf-8') as txt_data:
            result = txt_data.read().splitlines()
        assert len(data) == len(result)
        assert result[0].startswith('ID: 0')
        assert result[0].endswith('Company ID: 2')
