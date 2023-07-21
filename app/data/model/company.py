from app.data.model.employee import Employee
from dataclasses import dataclass, field
from typing import Any, Self


@dataclass(frozen=True, order=True)
class Company:
    """
    Represents a company entity.

    Attributes:
        id_ (int): The unique identifier of the company.
        company_name (str): The name of the company.
        street (str): The street address of the company.
        city (str): The city where the company is located.
        postal_code (int): The postal code of the company's address.
        state (str): The state or province where the company is located.
        country (str): The country where the company is located.
        employees (List[int | Employee]): A list of employee IDs or Employee objects associated with the company.
    """

    id_: int
    company_name: str
    street: str
    city: str
    postal_code: int
    state: str
    country: str
    employees: list[int | Employee] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the Company object to a dictionary representation.

        Returns:
            dict[str, Any]: A dictionary containing the attributes of the Company object.
        """
        return {
            'id': self.id_,
            'company_name': self.company_name,
            'street': self.street,
            'city': self.city,
            'postal_code': self.postal_code,
            'state': self.state,
            'country': self.country,
            'employees': [employee if isinstance(employee, int) else employee.to_dict() for employee in self.employees]
        }

    def __str__(self) -> str:
        """
        Return a string representation of the Company object.

        Returns:
            str: A string containing formatted company information.
        """
        return f"""ID: {self.id_}
Company Name: {self.company_name}
Street: {self.street}
City: {self.city}
Postal Code: {self.postal_code}
State: {self.state}
Country: {self.country}
Employees: {self.employees}"""

    def __repr__(self) -> str:
        """
        Return a string representation of the Company object (same as __str__).

        Returns:
            str: A string containing formatted company information.
        """
        return self.__str__()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Create a Company object from a dictionary representation.

        Args:
            data (dict[str, Any]): A dictionary containing the attributes of the Company object.

        Returns:
            Company: A new Company object created from the dictionary data.
        """
        data['id_'] = int(data.pop('id'))
        return cls(**data)
