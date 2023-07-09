from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Self


@dataclass(frozen=True, order=True)
class Employee:
    id: int
    first_name: str
    last_name: str
    position: str
    age: int
    employment_tenure: int
    department: str
    salary: Decimal
    performance_rating: dict[str, int]
    company_id: int

    def __str__(self) -> str:
        return f"""ID: {self.id}
First Name: {self.first_name}
Last Name: {self.last_name}
Position: {self.position}
Age: {self.age}
Employment Tenure: {self.employment_tenure}
Department: {self.department}
Salary: {self.salary}
Performance Rating: {self.performance_rating}
Company ID: {self.company_id}"""

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def from_dict(cls: Self, data: dict[str, Any]) -> Self:
        data['salary'] = Decimal(data['salary'])
        return cls(**data)


