from app.service.company import CompanyService
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
        try:
            company = CompanyService().get_company_by_name(company_name)
            return make_response(company.to_dict(), 200)
        except Exception as e:
            return make_response({'message': e.args[0]}, 400)

    def post(self, company_name: str) -> Response:
        data = CompanyResource.parser.parse_args()
        try:
            CompanyService().add_company(data | {'company_name': company_name})
            return make_response({'message': 'Company added'}, 201)
        except Exception as e:
            return make_response({'message': e.args[0]}, 400)

    def put(self, company_name: str) -> Response:
        data = CompanyResource.parser.parse_args()
        try:
            CompanyService().update_company(data | {'company_name': company_name})
            return make_response({'message': 'Company updated'}, 201)
        except Exception as e:
            return make_response({'message': e.args[0]}, 400)

    def delete(self, company_name: str) -> Response:
        try:
            CompanyService().delete_company(company_name)
            return make_response({'message': 'Company deleted'})
        except Exception as e:
            return make_response({'message': e.args[0]}, 400)


class CompanyListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('companies', type=list, required=True, help='No data provided', location='json')

    def get(self) -> Response:
        companies = CompanyService().get_all_companies()
        return make_response({'companies': [company.to_dict() for company in companies]}, 200)

    def post(self) -> Response:
        parsed = CompanyListResource.parser.parse_args()
        try:
            CompanyService().add_or_update_many(parsed.get('companies'))
            return make_response({'message': 'Companies added'}, 201)
        except Exception as e:
            return make_response({'message': e.args[0]}, 400)
