from app.security.token_required import jwt_required_with_roles
from app.service.employee import EmployeeService
from flask_restful import Resource, reqparse
from flask import make_response, Response


class EmployeeResource(Resource):
    """
    Resource for handling individual employee operations.

    This class provides endpoints and functionality for performing CRUD operations on individual employee records.

    Attributes:
        parser (reqparse.RequestParser): A request parser for handling incoming JSON data.
    """

    parser = reqparse.RequestParser()
    parser.add_argument('position', type=str)
    parser.add_argument('age', type=str)
    parser.add_argument('employment_tenure', type=str)
    parser.add_argument('department', type=str)
    parser.add_argument('salary', type=str)
    parser.add_argument('performance_rating', type=dict)
    parser.add_argument('company_id', type=str)

    def get(self, full_name: str) -> Response:
        """
        Retrieve employee information by full name.

        Args:
            full_name (str): The full name of the employee to retrieve.

        Returns:
            Response: A response containing the employee information or an error message.
        """
        try:
            employee = EmployeeService().get_employee_by_name(full_name)
            return make_response(employee.to_dict(), 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['user', 'admin'])
    def post(self, full_name: str) -> Response:
        """
        Create a new employee with the given full name and data.

        Args:
            full_name (str): The full name of the new employee.

        Returns:
            Response: A response containing the created employee information or an error message.
        """
        data = EmployeeResource.parser.parse_args()
        try:
            employee = EmployeeService().add_employee(data | {'full_name': full_name})
            return make_response(employee.to_dict(), 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['user', 'admin'])
    def put(self, full_name: str) -> Response:
        """
        Update employee information by full name.

        Args:
            full_name (str): The full name of the employee to update.

        Returns:
            Response: A response containing the updated employee information or an error message.
        """
        data = EmployeeResource.parser.parse_args()
        try:
            employee = EmployeeService().update_employee(data | {'full_name': full_name})
            return make_response(employee.to_dict(), 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['user', 'admin'])
    def delete(self, full_name: str) -> Response:
        """
        Delete an employee by full name.

        Args:
            full_name (str): The full name of the employee to delete.

        Returns:
            Response: A response indicating the result of the deletion or an error message.
        """
        try:
            id_ = EmployeeService().delete_employee(full_name)
            return make_response({'message': f'Deleted employee with id: {id_}'})
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)


class EmployeeListResource(Resource):
    """
    Resource for handling multiple employee operations.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('employees', type=list, required=True, help='No data provided', location='json')

    def get(self) -> Response:
        """
        Retrieve a list of all employees.

        Returns:
            Response: A response containing a list of employees or an error message.
        """
        employees = EmployeeService().get_all_employees()
        return make_response({'employees': [employee.to_dict() for employee in employees]}, 200)

    @jwt_required_with_roles(['user', 'admin'])
    def post(self) -> Response:
        """
        Create or update multiple employees with the provided data.

        Returns:
            Response: A response containing the created or updated employees or an error message.
        """
        parsed = EmployeeListResource.parser.parse_args()
        try:
            employees = EmployeeService().add_or_update_many(parsed.get('employees'))
            return make_response({'employees': [employee.to_dict() for employee in employees]}, 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)
