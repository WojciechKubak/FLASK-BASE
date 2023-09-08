from app.model.employee import EmployeeModel
from app.db.configuration import sa
from flask import Flask
from typing import Any


class TestEmployeeModelCrudMethods:

    def test_add(self, app: Flask, employee_model_data: dict[str, Any]) -> None:
        with app.app_context():
            employee = EmployeeModel(**employee_model_data)
            sa.session.add(employee)
            sa.session.commit()

            expected = sa.session.query(EmployeeModel).filter_by(id=employee.id).first()

            assert expected == employee

    def test_delete(self, app: Flask) -> None:
        with app.app_context():
            sa.session.add(employee := EmployeeModel(full_name='Employee'))
            sa.session.commit()

            employee.delete()

            assert not sa.session.query(EmployeeModel).filter_by(id=employee.id).first()

    def test_update(self, app: Flask) -> None:
        with app.app_context():
            sa.session.add(employee := EmployeeModel(full_name='Employee'))
            sa.session.commit()

            changes = {'age': 45}
            employee.update(changes)

            assert changes['age'] == employee.age

    def test_find_by_name(self, app: Flask) -> None:
        with app.app_context():
            sa.session.add(employee := EmployeeModel(full_name='Employee'))
            sa.session.commit()

            assert employee == EmployeeModel.find_by_name(employee.full_name)
