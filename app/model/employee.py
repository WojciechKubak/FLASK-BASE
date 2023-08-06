from app.db.configuration import sa
from decimal import Decimal
from typing import Any, Self


class EmployeeModel(sa.Model):

    __tablename__ = 'employees'

    id = sa.Column(sa.Integer, primary_key=True)
    full_name = sa.Column(sa.String(255))
    position = sa.Column(sa.String(255))
    age = sa.Column(sa.Integer)
    employment_tenure = sa.Column(sa.Integer)
    department = sa.Column(sa.String(255))
    salary = sa.Column(sa.Numeric(precision=6, scale=2))
    performance_rating = sa.Column(sa.JSON)
    company_id = sa.Column(sa.Integer, sa.ForeignKey('companies.id'))

    company = sa.relationship('CompanyModel', backref=sa.backref('employees'), lazy=True)

    def __init__(
            self,
            full_name: str,
            position: str,
            age: int,
            employment_tenure: int,
            department: str,
            salary: Decimal,
            performance_rating: dict[str, Any],
            company_id: int
    ):
        self.full_name = full_name
        self.position = position
        self.age = age
        self.employment_tenure = employment_tenure
        self.department = department
        self.salary = salary
        self.performance_rating = performance_rating
        self.company_id = company_id

    def to_dict(self) -> dict[str, Any]:
        return {
            'full_name': self.full_name,
            'position': self.position,
            'age': self.age,
            'employment_tenure': self.employment_tenure,
            'department': self.department,
            'salary': self.salary,
            'performance_rating': self.performance_rating,
            'company_id': self.company_id
        }

    def add(self) -> None:
        sa.session.add(self)
        sa.session.commit()

    def update(self, data: dict[str, Any]) -> None:
        for field_name, value in data.items():
            if hasattr(self, field_name):
                setattr(self, field_name, value)
        sa.session.commit()

    def delete(self) -> None:
        sa.session.delete(self)
        sa.session.commit()

    @classmethod
    def find_by_name(cls: Self, name: str) -> Self:
        return EmployeeModel.query.filter_by(full_name=name).first()
