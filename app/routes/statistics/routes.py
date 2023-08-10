from app.routes.statistics.service import StatisticsService
from flask import make_response, Response
from flask import Blueprint

statistics_blueprint = Blueprint('statistics', __name__, url_prefix='/statistics')


@statistics_blueprint.route('/employees_performance')
def employees_performance() -> Response:
    return make_response(StatisticsService.get_employees_overall_performance(), 200)


@statistics_blueprint.route('/best_and_worst_performing_employees')
def best_and_worst_performing_employees() -> Response:
    result = StatisticsService.get_best_and_worst_performing_employees()
    return make_response(result if result else {'message': 'No data available.'}, 200)


@statistics_blueprint.route('/departments_performance')
def departments_performance() -> Response:
    return make_response(StatisticsService.get_department_performance_overview(), 200)


@statistics_blueprint.route('/employees_avg_salary')
def employees_avg_salary() -> Response:
    return make_response(StatisticsService.get_employees_with_highest_and_lowest_salary(), 200)


@statistics_blueprint.route('/departments_salary')
def departments_salary() -> Response:
    return make_response(StatisticsService.get_department_employee_salary_overview(), 200)
