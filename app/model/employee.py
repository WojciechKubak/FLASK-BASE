from app.db.configuration import sa
from decimal import Decimal
from typing import Any, Self
from sqlalchemy.orm import Mapped, mapped_column


class EmployeeModel(sa.Model):

    __tablename__ = 'employees'

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    position: Mapped[str]
    age: Mapped[int]
    employment_tenure: Mapped[int]
    department: Mapped[int]
    salary: Mapped[Decimal]
    performance_rating: Mapped[dict[str, Any]] = mapped_column(type_=sa.JSON)
    company_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey('companies.id'))

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

    def get_performance_average(self) -> Any:
        ratings = list(self.performance_rating.values())
        if len(ratings) == 1:
            return ratings[0]
        return sum(ratings) / len(ratings) if ratings else None

    @classmethod
    def find_by_name(cls: Self, name: str) -> Self:
        return EmployeeModel.query.filter_by(full_name=name).first()
