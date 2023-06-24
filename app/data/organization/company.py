from dataclasses import dataclass
from typing import Any, Self


# todo: kolejność metod w klasie - jak pukładać kolejnoscią statyczne, magic, itp., jest jakieś źródło do tego?
@dataclass(frozen=True, order=True)
class Company:
    id: int
    company_name: str
    street: str
    city: str
    postal_code: int
    state: str
    country: str

    def __str__(self) -> str:
        return f"""
            ID: {self.id}
            Company Name: {self.company_name}
            Street: {self.street}
            City: {self.city}
            Postal Code: {self.postal_code}
            State: {self.state}
            Country: {self.country}
        """

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def from_dict(cls: Self, data: dict[str, Any]) -> Self:
        return cls(**data)



