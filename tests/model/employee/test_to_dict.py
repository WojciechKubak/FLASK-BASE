from app.model.employee import EmployeeModel
from app.db.configuration import sa
from flask import Flask
from typing import Any


def test_if_employee_model_to_dict_returns_expected_values(app: Flask, employee_model_data: dict[str, Any]) -> None:
    with app.app_context():
        sa.session.add(EmployeeModel(**employee_model_data))
        sa.session.commit()

        result = sa.session.query(EmployeeModel).filter_by(full_name=employee_model_data['full_name']).first().to_dict()

        assert all([v == result[k] for k, v in employee_model_data.items()])
