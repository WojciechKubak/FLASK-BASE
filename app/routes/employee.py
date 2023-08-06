from app.model.employee import EmployeeModel
from flask_restful import Resource, reqparse
from flask import make_response, Response
from decimal import Decimal


class EmployeeResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('position', type=str, required=True, help='Position field required')
    parser.add_argument('age', type=int, required=True, help='Age field required')
    parser.add_argument('employment_tenure', type=int, required=True, help='Employment tenure field required')
    parser.add_argument('department', type=str, required=True, help='Department field required')
    parser.add_argument('salary', type=Decimal, required=True, help='Salary field required')
    parser.add_argument('performance_rating', type=dict, required=True, help='Performance rating field required')
    parser.add_argument('company_id', type=int, required=True, help='Company id field required')

    @staticmethod
    def get(full_name: str) -> Response:
        result = EmployeeModel.filter_by(('full_name', full_name))
        if result:
            return make_response(result.to_dict(), 200)
        return make_response({'message': f'Employee: {full_name} not found'}, 400)

    @staticmethod
    def post(full_name: str) -> Response:
        if EmployeeModel.filter_by(('full_name', full_name)):
            return make_response({'message': f'Employee: {full_name} already exists'})
        data = EmployeeResource.parser.parse_args()
        try:
            employee = EmployeeModel(full_name, **data)
            employee.add_or_update()
            return make_response(employee.to_dict(), 201)
        except Exception:
            return make_response({'message': 'Error occurred'}, 400)

    @staticmethod
    def put(full_name: str) -> Response:
        if result := EmployeeModel.filter_by(('full_name', full_name)):
            try:
                for field_name, value in EmployeeResource.parser.parse_args().items():
                    setattr(result, field_name, value)
                result.add_or_update()
                return make_response(result.to_dict(), 200)
            except Exception:
                return make_response({'message': 'Error occurred'}, 400)
        return make_response({'message': f'Employee: {full_name} does not exist'}, 400)

    @staticmethod
    def delete(full_name: str) -> Response:
        if result := EmployeeModel.filter_by(('full_name', full_name)):
            result.delete()
            return make_response({'message': f'Employee: {full_name} deleted'}, 200)
        return make_response({'message': f'Employee: {full_name} does not exist'}, 400)
