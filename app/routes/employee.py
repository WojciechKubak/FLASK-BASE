from app.service.employee import EmployeeService
from flask_restful import Resource, reqparse
from flask import make_response, Response
from decimal import Decimal


class EmployeeResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('position', type=str, required=True, help='position field required')
    parser.add_argument('age', type=int, required=True, help='age field required')
    parser.add_argument('employment_tenure', type=int, required=True, help='employment_tenure field required')
    parser.add_argument('department', type=str, required=True, help='department field required')
    parser.add_argument('salary', type=Decimal, required=True, help='salary field required')
    parser.add_argument('performance_rating', type=dict, required=True, help='performance_rating field required')
    parser.add_argument('company_id', type=int, required=True, help='company_id field required')

    def get(self, full_name: str) -> Response:
        try:
            employee = EmployeeService().get_employee_by_name(full_name)
            return make_response(employee.to_dict(), 200)
        except Exception as e:
            return make_response({'message': e.args[0]}, 400)

    def post(self, full_name: str) -> Response:
        data = EmployeeResource.parser.parse_args()
        try:
            EmployeeService().add_employee(data | {'full_name': full_name})
            return make_response({'message': 'Employee added'}, 201)
        except Exception as e:
            return make_response({'message': e.args[0]}, 400)

    def put(self, full_name: str) -> Response:
        data = EmployeeResource.parser.parse_args()
        try:
            EmployeeService().update_employee(data | {'full_name': full_name})
            return make_response({'message': 'Employee updated'}, 201)
        except Exception as e:
            return make_response({'message': e.args[0]}, 400)

    def delete(self, full_name: str) -> Response:
        try:
            EmployeeService().delete_employee(full_name)
            return make_response({'message': 'Employee deleted'})
        except Exception as e:
            return make_response({'message': e.args[0]}, 400)


class EmployeeListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('employees', type=list, required=True, help='No data provided', location='json')

    def get(self) -> Response:
        employees = EmployeeService().get_all_employees()
        return make_response({'employees': [employee.to_dict() for employee in employees]}, 200)

    def post(self) -> Response:
        parsed = EmployeeListResource.parser.parse_args()
        try:
            EmployeeService().add_or_update_many(parsed.get('employees'))
            return make_response({'message': 'Employees added'}, 201)
        except Exception as e:
            return make_response({'message': e.args[0]}, 400)
