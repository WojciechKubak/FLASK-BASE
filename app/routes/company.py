from app.model.company import CompanyModel
from flask_restful import Resource, reqparse
from flask import make_response, Response


class CompanyResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('street', type=str, required=True, help='Street field required')
    parser.add_argument('city', type=str, required=True, help='City field required')
    parser.add_argument('postal_code', type=str, required=True, help='Postal code field required')
    parser.add_argument('state', type=str, required=True, help='State field required')
    parser.add_argument('country', type=str, required=True, help='Country field required')

    @staticmethod
    def get(company_name: str) -> Response:
        result = CompanyModel.filter_by(('company_name', company_name))
        if result:
            return make_response(result.to_dict(), 200)
        return make_response({'message': f'Company: {company_name} not found'}, 400)

    @staticmethod
    def post(company_name: str) -> Response:
        if CompanyModel.filter_by(('company_name', company_name)):
            return make_response({'message': f'Company: {company_name} already exists'})
        data = CompanyResource.parser.parse_args()
        try:
            company = CompanyModel(company_name, **data)
            company.add_or_update()
            return make_response(company.to_dict(), 201)
        except Exception:
            return make_response({'message': 'Error occurred'}, 400)

    @staticmethod
    def put(company_name: str) -> Response:
        if result := CompanyModel.filter_by(('company_name', company_name)):
            try:
                for field_name, value in CompanyResource.parser.parse_args().items():
                    setattr(result, field_name, value)
                result.add_or_update()
                return make_response(result.to_dict(), 200)
            except Exception:
                return make_response({'message': 'Error occurred'}, 400)
        return make_response({'message': f'Company: {company_name} does not exist'}, 400)

    @staticmethod
    def delete(company_name: str) -> Response:
        if result := CompanyModel.filter_by(('company_name', company_name)):
            result.delete()
            return make_response({'message': f'Company: {company_name} deleted'}, 200)
        return make_response({'message': f'Company: {company_name} does not exist'}, 400)
