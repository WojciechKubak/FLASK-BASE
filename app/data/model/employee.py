from app.data.model.company import Company
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Self


@dataclass(frozen=True, order=True)
class Employee:
    id_: int
    first_name: str
    last_name: str
    position: str
    age: int
    employment_tenure: int
    department: str
    salary: Decimal
    performance_rating: dict[str, int]
    company: int | Company

    def get_performance_average(self) -> float:
        ratings = list(self.performance_rating.values())
        return sum(ratings) / len(ratings)

    def __str__(self) -> str:
        return f"""ID: {self.id_}
First Name: {self.first_name}
Last Name: {self.last_name}
Position: {self.position}
Age: {self.age}
Employment Tenure: {self.employment_tenure}
Department: {self.department}
Salary: {self.salary}
Performance Rating: {self.performance_rating}
Company ID: {self.company}"""

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def from_dict(cls: Self, data: dict[str, Any]) -> Self:
        data['id_'] = int(data.pop('id'))
        data['age'] = int(data['age'])
        data['salary'] = Decimal(data['salary'])
        # data['company_id'] =
        return cls(**data)
