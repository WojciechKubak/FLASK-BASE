from app.data.model.company import Company


class TestCompanyToDict:

    def test_id_name_conversion(self, company_with_no_employees_data: Company) -> None:
        assert 'id' in company_with_no_employees_data.to_dict()

    def test_when_no_employees_in_company(self, company_with_no_employees_data: Company) -> None:
        result = company_with_no_employees_data.to_dict()
        assert not result['employees']

    def test_when_employee_objects_in_company(self, company_with_employee_objects: Company) -> None:
        result = company_with_employee_objects.to_dict()
        assert len(company_with_employee_objects.employees) == len(result['employees'])
        assert all(isinstance(obj, dict) for obj in result['employees'])

    def test_when_employee_ids_in_company(self, company_with_employee_ids: Company) -> None:
        result = company_with_employee_ids.to_dict()
        assert len(company_with_employee_ids.employees) == len(result['employees'])
        assert all(isinstance(obj, int) for obj in result['employees'])
