from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Callable, Self


@dataclass(frozen=True, order=True)
class Employee:
    """
    Represents an employee entity.

    Attributes:
        id_ (int): The unique identifier of the employee.
        first_name (str): The first name of the employee.
        last_name (str): The last name of the employee.
        position (str): The position or job title of the employee.
        age (int): The age of the employee.
        employment_tenure (int): The tenure (in months) of the employee's employment.
        department (str): The department where the employee works.
        salary (Decimal): The salary of the employee.
        performance_rating (dict[str, int]): A dictionary containing performance ratings for the employee.
        company (int): The unique identifier of the company the employee belongs to.
    """

    id_: int
    first_name: str
    last_name: str
    position: str
    age: int
    employment_tenure: int
    department: str
    salary: Decimal
    performance_rating: dict[str, int]
    company: int

    def get_performance_average(self) -> Any:
        """
        Calculate the average performance rating for the employee.

        Returns:
            Any: The average performance rating or None if no ratings are available.
        """
        ratings = list(self.performance_rating.values())
        if len(ratings) == 1:
            return ratings[0]
        return sum(ratings) / len(ratings) if ratings else None

    def filter_by_criterion(self, criterion: tuple[str, Callable[[Any], bool]]) -> bool:
        """
        Check if the employee meets a specific criterion based on the provided attribute name and expression.

        Args:
            criterion (tuple[str, Callable[[Any], bool]]): A tuple containing the attribute name and an expression
                (function) that evaluates the attribute value.

        Returns:
            bool: True if the employee meets the criterion, False otherwise.

        Raises:
            AttributeError: If the attribute name is not found in the Employee object.
        """
        attr_name, expression = criterion
        if attr_name not in self.__dict__.keys():
            raise AttributeError('Key not found.')
        return expression(getattr(self, attr_name))

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the Employee object to a dictionary representation.

        Returns:
            dict[str, Any]: A dictionary containing the attributes of the Employee object.
        """
        return {
            'id': self.id_,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'position': self.position,
            'age': self.age,
            'employment_tenure': self.employment_tenure,
            'department': self.department,
            'salary': self.salary,
            'performance_rating': self.performance_rating,
            'company': self.company
        }

    def __str__(self) -> str:
        """
        Return a string representation of the Employee object.

        Returns:
            str: A string containing formatted employee information.
        """
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
        """
        Return a string representation of the Employee object (same as __str__).

        Returns:
            str: A string containing formatted employee information.
        """
        return self.__str__()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Create an Employee object from a dictionary representation.

        Args:
            data (dict[str, Any]): A dictionary containing the attributes of the Employee object.

        Returns:
            Employee: A new Employee object created from the dictionary data.
        """
        data['id_'] = int(data.pop('id'))
        data['age'] = int(data['age'])
        data['salary'] = Decimal(data['salary'])
        data['company'] = int(data['company'])
        data['performance_rating'] = {k: int(v) for k, v in data['performance_rating'].items()}
        return cls(**data)
