from app.model.employee import EmployeeModel
from app.db.configuration import sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime
from typing import Any, Self


class CompanyModel(sa.Model):
    """
    SQLAlchemy model representing a company.

    Attributes:
        id (Mapped[int]): Primary key for the company.
        name (Mapped[str]): Name of the company.
        street (Mapped[str]): Street address of the company.
        city (Mapped[str]): City where the company is located.
        postal_code (Mapped[str]): Postal code of the company's location.
        state (Mapped[str]): State or region where the company is located.
        country (Mapped[str]): Country where the company is located.
        employees (Mapped[list[EmployeeModel]]): List of employees associated with the company.
        created_at (Mapped[datetime]): Timestamp of when the company was created.
        updated_at (Mapped[datetime]): Timestamp of when the company was last updated.
    """

    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(sa.Integer(), primary_key=True)

    name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    street: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    city: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    postal_code: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    state: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    country: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    employees: Mapped[list[EmployeeModel]] = sa.relationship(EmployeeModel, backref='companies')

    created_at: Mapped[datetime] = mapped_column(insert_default=func.utc_timestamp())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.utc_timestamp(), onupdate=func.utc_timestamp())

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the company object to a dictionary.

        Returns:
            dict[str, Any]: A dictionary representation of the company.
        """
        return {
            'id': self.id,
            'name': self.name,
            'street': self.street,
            'city': self.city,
            'postal_code': self.postal_code,
            'state': self.state,
            'country': self.country,
            'employees': [employee.to_dict() for employee in self.employees]
        }

    def add(self) -> None:
        """
        Add the company to the database session and commit the transaction.

        Returns:
            None
        """
        sa.session.add(self)
        sa.session.commit()

    def update(self, data: dict[str, Any]) -> None:
        """
        Update the company's fields with the provided data and commit the transaction.

        Args:
            data (dict[str, Any]): The data to update the company with.

        Returns:
            None
        """
        for field_name, value in data.items():
            if hasattr(self, field_name):
                setattr(self, field_name, value)
        sa.session.commit()

    def delete(self) -> None:
        """
        Delete the company from the database session and commit the transaction.

        Returns:
            None
        """
        sa.session.delete(self)
        sa.session.commit()

    @classmethod
    def find_by_name(cls: Self, name: str) -> Self:
        """
        Find a company by its name.

        Args:
            name (str): The name of the company to find.

        Returns:
            Self: The found company object or None if not found.
        """
        return CompanyModel.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls: Self, id_: int) -> Self:
        """
        Find a company by its ID.

        Args:
            id_ (int): The ID of the company to find.

        Returns:
            Self: The found company object or None if not found.
        """
        return CompanyModel.query.filter_by(id=id_).first()
