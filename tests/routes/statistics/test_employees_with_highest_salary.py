from app.model.employee import EmployeeModel
from app.db.configuration import sa
from flask.testing import FlaskClient
from flask import Flask


class TestEmployeesWithHighestSalary:

    def test_when_no_data_available(self, client: FlaskClient, app: Flask) -> None:
        with app.app_context():
            sa.session.query(EmployeeModel).delete()
            sa.session.commit()

        response = client.get('/statistics/employees/salaries/highest')

        assert response.status_code == 200
        assert not response.json

    def test_when_data_available(self, client: FlaskClient, app: Flask) -> None:
        response = client.get('/statistics/employees/salaries/highest')

        with app.app_context():
            employees = sa.session.query(EmployeeModel).all()
            max_salary = max([e.salary for e in employees])
            expected = [e.to_dict() for e in employees if e.salary == max_salary]

        assert response.status_code == 200
        assert expected == response.json
