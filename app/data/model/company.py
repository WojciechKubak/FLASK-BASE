from dataclasses import dataclass
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

    def __str__(self) -> str:
        return f"""ID: {self.id_}
Company Name: {self.company_name}
Street: {self.street}
City: {self.city}
Postal Code: {self.postal_code}
State: {self.state}
Country: {self.country}"""

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def from_dict(cls: Self, data: dict[str, Any]) -> Self:
        data['id_'] = int(data.pop('id'))
        return cls(**data)

