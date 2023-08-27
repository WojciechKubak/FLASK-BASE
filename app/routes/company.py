from app.service.company import CompanyService
from app.security.token_required import token_required
from flask_restful import Resource, reqparse
from flask import make_response, Response


class CompanyResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('street', type=str)
    parser.add_argument('city', type=str)
    parser.add_argument('postal_code', type=str)
    parser.add_argument('state', type=str)
    parser.add_argument('country', type=str)

    def get(self, company_name: str) -> Response:
        try:
            company = CompanyService().get_company_by_name(company_name)
            return make_response(company.to_dict(), 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @token_required(['user', 'admin'])
    def post(self, company_name: str) -> Response:
        data = CompanyResource.parser.parse_args()
        try:
            company = CompanyService().add_company(data | {'name': company_name})
            return make_response(company.to_dict(), 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @token_required(['user', 'admin'])
    def put(self, company_name: str) -> Response:
        data = CompanyResource.parser.parse_args()
        try:
            company = CompanyService().update_company(data | {'name': company_name})
            return make_response(company.to_dict(), 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @token_required(['user', 'admin'])
    def delete(self, company_name: str) -> Response:
        try:
            id_ = CompanyService().delete_company(company_name)
            return make_response({'message': f'Deleted company with id: {id_}'})
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)


class CompanyListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('companies', type=list, required=True, help='No data provided', location='json')

    def get(self) -> Response:
        companies = CompanyService().get_all_companies()
        return make_response({'companies': [company.to_dict() for company in companies]}, 200)

    @token_required(['user', 'admin'])
    def post(self) -> Response:
        parsed = CompanyListResource.parser.parse_args()
        try:
            companies = CompanyService().add_or_update_many(parsed.get('companies'))
            return make_response({'companies': [company.to_dict() for company in companies]}, 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)
