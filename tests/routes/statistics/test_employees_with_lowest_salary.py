from app.model.employee import EmployeeModel
from app.db.configuration import sa
from flask.testing import FlaskClient
from flask import Flask


class TestEmployeesWithLowestSalary:

    def test_when_no_data_available(self, client: FlaskClient, app: Flask) -> None:
        with app.app_context():
            sa.session.query(EmployeeModel).delete()
            sa.session.commit()

        response = client.get('/statistics/employees/salaries/lowest')

        assert response.status_code == 200
        assert not response.json

    def test_when_data_available(self, client: FlaskClient, app: Flask) -> None:
        response = client.get('/statistics/employees/salaries/lowest')

        with app.app_context():
            employees = sa.session.query(EmployeeModel).all()
            min_salary = min([e.salary for e in employees])
            expected = [e.to_dict() for e in employees if e.salary == min_salary]

        assert response.status_code == 200
        assert expected == response.json
