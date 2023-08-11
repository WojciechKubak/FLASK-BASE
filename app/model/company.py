from app.model.employee import EmployeeModel
from app.db.configuration import sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime
from typing import Any, Self


class CompanyModel(sa.Model):

    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(sa.Integer(), primary_key=True)
    company_name: Mapped[str]
    street: Mapped[str]
    city: Mapped[str]
    postal_code: Mapped[str]
    state: Mapped[str]
    country: Mapped[str]
    employees: Mapped[list[EmployeeModel]] = sa.relationship(EmployeeModel, backref='companies')
    created_at: Mapped[datetime] = mapped_column(insert_default=func.utc_timestamp())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.utc_timestamp(), onupdate=func.utc_timestamp())

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
        return CompanyModel.query.filter_by(company_name=name).first()
