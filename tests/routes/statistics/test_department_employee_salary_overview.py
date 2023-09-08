from app.model.employee import EmployeeModel
from app.db.configuration import sa
from flask.testing import FlaskClient
from flask import Flask


class TestDepartmentEmployeeSalaryOvierview:

    def test_when_no_data_available(self, client: FlaskClient, app: Flask) -> None:
        with app.app_context():
            sa.session.query(EmployeeModel).delete()
            sa.session.commit()

        response = client.get('/statistics/departments/salary')

        assert 200 == response.status_code
        assert not response.json

    def test_when_data_available(self, client: FlaskClient, app: Flask) -> None:
        response = client.get('/statistics/departments/salary')

        with app.app_context():
            employees = sa.session.query(EmployeeModel).all()
            expected = {}
            for department in set([e.department for e in employees]):
                salaries = [e.salary for e in employees if e.department == department]
                expected[department] = sum(salaries) / len(salaries)

        assert 200 == response.status_code
        assert expected == response.json
