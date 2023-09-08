from app.db.configuration import sa
from app.model.employee import EmployeeModel
from flask.testing import FlaskClient
from flask import Flask


def test_employees_overall_performance(client: FlaskClient, app: Flask) -> None:
    response = client.get('statistics/employees/performance')

    with app.app_context():
        employees = sa.session.query(EmployeeModel).all()
        expected = {e.full_name: e.get_performance_average() for e in employees}

    assert 200 == response.status_code
    assert expected == response.json
