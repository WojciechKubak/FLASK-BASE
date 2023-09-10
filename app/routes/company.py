from app.security.token_required import jwt_required_with_roles
from app.service.company import CompanyService
from flask_restful import Resource, reqparse
from flask import make_response, Response


class CompanyResource(Resource):
    """
    Resource for handling individual company operations.

    This class provides endpoints and functionality for performing CRUD operations on individual company records.

    Attributes:
        parser (reqparse.RequestParser): A request parser for handling incoming JSON data.
    """

    parser = reqparse.RequestParser()
    parser.add_argument('street', type=str)
    parser.add_argument('city', type=str)
    parser.add_argument('postal_code', type=str)
    parser.add_argument('state', type=str)
    parser.add_argument('country', type=str)

    def get(self, company_name: str) -> Response:
        """
        Retrieve company information by name.

        Args:
            company_name (str): The name of the company to retrieve.

        Returns:
            Response: A response containing the company information or an error message.
        """
        try:
            company = CompanyService().get_company_by_name(company_name)
            return make_response(company.to_dict(), 200)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['user', 'admin'])
    def post(self, company_name: str) -> Response:
        """
        Create a new company with the given name and data.

        Args:
            company_name (str): The name of the new company.

        Returns:
            Response: A response containing the created company information or an error message.
        """
        data = CompanyResource.parser.parse_args()
        try:
            company = CompanyService().add_company(data | {'name': company_name})
            return make_response(company.to_dict(), 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['user', 'admin'])
    def put(self, company_name: str) -> Response:
        """
        Update company information by name.

        Args:
            company_name (str): The name of the company to update.

        Returns:
            Response: A response containing the updated company information or an error message.
        """
        data = CompanyResource.parser.parse_args()
        try:
            company = CompanyService().update_company(data | {'name': company_name})
            return make_response(company.to_dict(), 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)

    @jwt_required_with_roles(['user', 'admin'])
    def delete(self, company_name: str) -> Response:
        """
        Delete a company by name.

        Args:
            company_name (str): The name of the company to delete.

        Returns:
            Response: A response indicating the result of the deletion or an error message.
        """
        try:
            id_ = CompanyService().delete_company(company_name)
            return make_response({'message': f'Deleted company with id: {id_}'})
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)


class CompanyListResource(Resource):
    """
    Resource for handling multiple company operations.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('companies', type=list, required=True, help='No data provided', location='json')

    def get(self) -> Response:
        """
        Retrieve a list of all companies.

        Returns:
            Response: A response containing a list of companies or an error message.
        """
        companies = CompanyService().get_all_companies()
        return make_response({'companies': [company.to_dict() for company in companies]}, 200)

    @jwt_required_with_roles(['user', 'admin'])
    def post(self) -> Response:
        """
        Create or update multiple companies with the provided data.

        Returns:
            Response: A response containing the created or updated companies or an error message.
        """
        parsed = CompanyListResource.parser.parse_args()
        try:
            companies = CompanyService().add_or_update_many(parsed.get('companies'))
            return make_response({'companies': [company.to_dict() for company in companies]}, 201)
        except ValueError as e:
            return make_response({'message': e.args[0]}, 400)
