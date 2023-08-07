from app.model.company import CompanyModel
from flask_restful import Resource, reqparse
from flask import make_response, Response


class CompanyResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('street', type=str, required=True, help='street field required')
    parser.add_argument('city', type=str, required=True, help='city field required')
    parser.add_argument('postal_code', type=str, required=True, help='postal_code code field required')
    parser.add_argument('state', type=str, required=True, help='state field required')
    parser.add_argument('country', type=str, required=True, help='country field required')

    def get(self, company_name: str) -> Response:
        result = CompanyModel.find_by_name(company_name)
        if result:
            return make_response(result.to_dict(), 200)
        return make_response({'message': f'Company: {company_name} not found'}, 400)

    def post(self, company_name: str) -> Response:
        if CompanyModel.find_by_name(company_name):
            return make_response({'message': f'Company: {company_name} already exists'})
        data = CompanyResource.parser.parse_args()
        try:
            company = CompanyModel(company_name=company_name, **data)
            company.add()
            return make_response(company.to_dict(), 201)
        except Exception:
            return make_response({'message': 'Error occurred'}, 400)

    def put(self, company_name: str) -> Response:
        if result := CompanyModel.find_by_name(company_name):
            data = CompanyResource.parser.parse_args()
            try:
                result.update(data)
                return make_response({'message': 'Record updated successfully'}, 200)
            except Exception:
                return make_response({'message': 'Error occurred'}, 400)
        return make_response({'message': f'Company: {company_name} does not exist'}, 400)

    def delete(self, company_name: str) -> Response:
        if result := CompanyModel.find_by_name(company_name):
            result.delete()
            return make_response({'message': f'Company: {company_name} deleted'}, 200)
        return make_response({'message': f'Company: {company_name} does not exist'}, 400)


class CompanyListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('companies', type=list, required=True, help='No data provided', location='json')

    def get(self) -> Response:
        return make_response({'companies': [company.to_dict() for company in CompanyModel.query.all()]}, 200)

    def post(self) -> Response:
        parsed = CompanyListResource.parser.parse_args()
        for data in parsed.get('companies'):
            if result := CompanyModel.find_by_name(data.get('company_name')):
                result.update(data)
            else:
                CompanyModel(**data).add()
        return make_response({'message': 'Records added successfully'}, 201)
