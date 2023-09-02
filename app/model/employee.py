from app.db.configuration import sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime
from decimal import Decimal
from typing import Any, Self


class EmployeeModel(sa.Model):

    __tablename__ = 'employees'

    id: Mapped[int] = mapped_column(sa.Integer(), primary_key=True)

    full_name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    position: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    age: Mapped[int] = mapped_column(sa.Integer(), nullable=True)
    employment_tenure: Mapped[int] = mapped_column(sa.Integer(), default=0)
    department: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    salary: Mapped[Decimal] = mapped_column(sa.Numeric(precision=8, scale=2), nullable=True)
    performance_rating: Mapped[dict[str, Any]] = mapped_column(type_=sa.JSON, nullable=True)
    company_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey('companies.id'), nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=func.utc_timestamp())
    updated_at: Mapped[datetime] = mapped_column(default=func.utc_timestamp(), onupdate=func.utc_timestamp())

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'full_name': self.full_name,
            'position': self.position,
            'age': self.age,
            'employment_tenure': self.employment_tenure,
            'department': self.department,
            'salary': float(self.salary),
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

    def get_performance_average(self) -> Any:
        ratings = list(self.performance_rating.values())
        if len(ratings) == 1:
            return ratings[0]
        return sum(ratings) / len(ratings) if ratings else None

    @classmethod
    def find_by_name(cls: Self, name: str) -> Self:
        return EmployeeModel.query.filter_by(full_name=name).first()
