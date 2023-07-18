from app.data.model.employee import Employee
from dataclasses import dataclass, field
from typing import Any, Self


@dataclass(frozen=True, order=True)
class Company:
    id_: int
    company_name: str
    street: str
    city: str
    postal_code: int
    state: str
    country: str
    employees: list[int | Employee] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
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
        return f"""ID: {self.id_}
Company Name: {self.company_name}
Street: {self.street}
City: {self.city}
Postal Code: {self.postal_code}
State: {self.state}
Country: {self.country}
Employees: {self.employees}"""

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def from_dict(cls: Self, data: dict[str, Any]) -> Self:
        data['id_'] = int(data.pop('id'))
        return cls(**data)
