from app.service.service.employee import EmployeeService
from app.service.additional.exporter import FileExportFormat
import json


class TestExportData:

    def test_when_exporting_to_txt_file(self, export_txt_path: str, employee_service: EmployeeService) -> None:
        employee_service.export_data(export_txt_path, FileExportFormat.TXT_FILE)
        with open(export_txt_path, 'r', encoding='utf-8') as txt_data:
            result = txt_data.read().splitlines()
        assert len(employee_service.find_all()) == len(result)

    def test_when_exporting_to_json_file(self, export_json_path: str, employee_service: EmployeeService) -> None:
        employee_service.export_data(export_json_path, FileExportFormat.JSON_FILE)
        with open(export_json_path, 'r', encoding='utf-8') as json_data:
            result = json.load(json_data)
        assert len(employee_service.find_all()) == len(result)
