from app.db.configuration import sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime
from decimal import Decimal
from typing import Any, Self


class EmployeeModel(sa.Model):
    """
    SQLAlchemy model representing an employee.

    Attributes:
        id (Mapped[int]): Primary key for the employee.
        full_name (Mapped[str]): Full name of the employee.
        position (Mapped[str]): Position/title of the employee.
        age (Mapped[int]): Age of the employee.
        employment_tenure (Mapped[int]): Employment tenure (in months) of the employee.
        department (Mapped[str]): Department where the employee works.
        salary (Mapped[Decimal]): Salary of the employee.
        performance_rating (Mapped[dict[str, Any]]): Performance ratings of the employee.
        company_id (Mapped[int]): ID of the company to which the employee belongs.
        created_at (Mapped[datetime]): Timestamp of when the employee record was created.
        updated_at (Mapped[datetime]): Timestamp of when the employee record was last updated.
    """

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

    def __eq__(self, other: Self) -> bool:
        """
        Compare two EmployeeModel objects based on their identifiers.

        Args:
            other (EmployeeModel): Another EmployeeModel object to compare with the current one.

        Returns:
            bool: True if the identifiers of the objects are the same, otherwise False.
        """
        return self.to_dict() == other.to_dict()

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the employee object to a dictionary.

        Returns:
            dict[str, Any]: A dictionary representation of the employee.
        """
        return {
            'id': self.id,
            'full_name': self.full_name,
            'position': self.position,
            'age': self.age,
            'employment_tenure': self.employment_tenure,
            'department': self.department,
            'salary': float(self.salary) if self.salary else None,
            'performance_rating': self.performance_rating,
            'company_id': self.company_id
        }

    def add(self) -> None:
        """
        Add the employee to the database session and commit the transaction.

        Returns:
            None
        """
        sa.session.add(self)
        sa.session.commit()

    def update(self, data: dict[str, Any]) -> None:
        """
        Update the employee's fields with the provided data and commit the transaction.

        Args:
            data (dict[str, Any]): The data to update the employee with.

        Returns:
            None
        """
        for field_name, value in data.items():
            if hasattr(self, field_name):
                setattr(self, field_name, value)
        sa.session.commit()

    def delete(self) -> None:
        """
        Delete the employee from the database session and commit the transaction.

        Returns:
            None
        """
        sa.session.delete(self)
        sa.session.commit()

    def get_performance_average(self) -> Any:
        """
        Calculate and return the average performance rating of the employee.

        Returns:
            Any: The average performance rating or None if no ratings are available.
        """
        ratings = list(self.performance_rating.values())
        if len(ratings) == 1:
            return ratings[0]
        return sum(ratings) / len(ratings) if ratings else None

    @classmethod
    def find_by_name(cls: Self, name: str) -> Self:
        """
        Find an employee by their full name.

        Args:
            name (str): The full name of the employee to find.

        Returns:
            Self: The found employee object or None if not found.
        """
        return EmployeeModel.query.filter_by(full_name=name).first()
