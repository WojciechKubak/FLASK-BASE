from app.service.employee import EmployeeService
from app.security.token_required import token_required
from flask_restful import Resource, reqparse
from flask import make_response, Response


class EmployeeResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('position', type=str)
    parser.add_argument('age', type=str)
    parser.add_argument('employment_tenure', type=str)
    parser.add_argument('department', type=str)
    parser.add_argument('salary', type=str)
    parser.add_argument('performance_rating', type=dict)
    parser.add_argument('company_id', type=str)

    def get(self, full_name: str) -> Response:
        try:
            employee = EmployeeService().get_employee_by_name(full_name)
            return make_response(employee.to_dict(), 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @token_required(['user', 'admin'])
    def post(self, full_name: str) -> Response:
        data = EmployeeResource.parser.parse_args()
        try:
            employee = EmployeeService().add_employee(data | {'full_name': full_name})
            return make_response(employee.to_dict(), 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @token_required(['user', 'admin'])
    def put(self, full_name: str) -> Response:
        data = EmployeeResource.parser.parse_args()
        try:
            employee = EmployeeService().update_employee(data | {'full_name': full_name})
            return make_response(employee.to_dict(), 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @token_required(['user', 'admin'])
    def delete(self, full_name: str) -> Response:
        try:
            id_ = EmployeeService().delete_employee(full_name)
            return make_response({'message': f'Deleted employee with id: {id_}'})
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)


class EmployeeListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('employees', type=list, required=True, help='No data provided', location='json')

    def get(self) -> Response:
        employees = EmployeeService().get_all_employees()
        return make_response({'employees': [employee.to_dict() for employee in employees]}, 200)

    @token_required(['user', 'admin'])
    def post(self) -> Response:
        parsed = EmployeeListResource.parser.parse_args()
        try:
            employees = EmployeeService().add_or_update_many(parsed.get('employees'))
            return make_response({'employees': [employee.to_dict() for employee in employees]}, 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)
