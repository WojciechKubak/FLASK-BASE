from app.db.configuration import sa
from typing import Any, Self


class CompanyModel(sa.Model):

    __tablename__ = 'companies'

    id = sa.Column(sa.Integer, primary_key=True)
    company_name = sa.Column(sa.String(255))
    street = sa.Column(sa.String(255))
    city = sa.Column(sa.String(255))
    postal_code = sa.Column(sa.String(20))
    state = sa.Column(sa.String(20))
    country = sa.Column(sa.String(255))

    def __init__(self, company_name: str, street: str, city: str, postal_code: str, state: str, country: str):
        self.company_name = company_name
        self.street = street
        self.city = city
        self.postal_code = postal_code
        self.state = state
        self.country = country

    def to_dict(self) -> dict[str, Any]:
        return {
            'company': self.company_name,
            'street': self.street,
            'city': self.city,
            'postal_code': self.postal_code,
            'state': self.state,
            'country': self.country,
            'employees': [employee.to_dict() for employee in self.employees]
        }

    def add_or_update(self) -> None:
        sa.session.add(self)
        sa.session.commit()

    def delete(self) -> None:
        sa.session.delete(self)
        sa.session.commit()

    @classmethod
    def filter_by(cls: Self, criterion: tuple[str, Any]) -> Self:
        field_name, _ = criterion
        if field_name not in cls.__dict__.keys():
            raise AttributeError('Field name not found.')
        return CompanyModel.query.filter_by(**dict([criterion])).first()
