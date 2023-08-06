from app.model.employee import EmployeeModel
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

    @staticmethod
    def get(full_name: str) -> Response:
        result = EmployeeModel.find_by_name(full_name)
        if result:
            return make_response(result.to_dict(), 200)
        return make_response({'message': f'Employee: {full_name} not found'}, 400)

    @staticmethod
    def post(full_name: str) -> Response:
        if EmployeeModel.find_by_name(full_name):
            return make_response({'message': f'Employee: {full_name} already exists'})
        data = EmployeeResource.parser.parse_args()
        try:
            employee = EmployeeModel(full_name, **data)
            employee.add()
            return make_response(employee.to_dict(), 201)
        except Exception:
            return make_response({'message': 'Error occurred'}, 400)

    @staticmethod
    def put(full_name: str) -> Response:
        if result := EmployeeModel.find_by_name(full_name):
            data = EmployeeResource.parser.parse_args()
            try:
                result.update(data)
                return make_response({'message': 'Record updated successfully'}, 200)
            except Exception:
                return make_response({'message': 'Error occurred'}, 400)
        return make_response({'message': f'Employee: {full_name} does not exist'}, 400)

    @staticmethod
    def delete(full_name: str) -> Response:
        if result := EmployeeModel.find_by_name(full_name):
            result.delete()
            return make_response({'message': f'Employee: {full_name} deleted'}, 200)
        return make_response({'message': f'Employee: {full_name} does not exist'}, 400)


class EmployeeListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('employees', type=list, required=True, help='No data provided', location='json')

    @staticmethod
    def get() -> Response:
        return make_response({'employees': [employee.to_dict() for employee in EmployeeModel.query.all()]}, 200)

    @staticmethod
    def post() -> Response:
        parsed = EmployeeListResource.parser.parse_args()
        for data in parsed.get('employees'):
            if result := EmployeeModel.find_by_name(data.get('full_name')):
                result.update(data)
            else:
                EmployeeModel(**data).add()
        return make_response({'message': 'Records added successfully'}, 201)
