from flask import make_response
from flask import Blueprint

statistics_blueprint = Blueprint('statistics', __name__, url_prefix='/statistics')


@statistics_blueprint.route('/best_and_worst_employees')
def get_best_and_worst_performing_employees():
    return make_response({})


@statistics_blueprint.route('/department_performance_overview')
def get_department_performance_overview():
    ...


@statistics_blueprint.route('/employee_avg_salary')
def get_employees_salary_average_mean():
    ...


@statistics_blueprint.route('/employees_salary')
def get_employees_with_highest_and_lowest_salary():
    ...


@statistics_blueprint.route('/department_salary')
def get_department_employee_salary_overview():
    ...
