from app.service.statistics import StatisticsService
from flask import make_response, Response
from flask import Blueprint

statistics_blueprint = Blueprint('statistics', __name__, url_prefix='/statistics')
employees_blueprint = Blueprint('employees', __name__, url_prefix='/employees')
departments_blueprint = Blueprint('departments', __name__, url_prefix='/departments')
salaries_blueprint = Blueprint('salaries', __name__, url_prefix='/salaries')

statistics_blueprint.register_blueprint(employees_blueprint)
statistics_blueprint.register_blueprint(departments_blueprint)
employees_blueprint.register_blueprint(salaries_blueprint)


@employees_blueprint.route('/performance', methods=['GET'])
def employees_overall_performance() -> Response:
    performance = StatisticsService().get_employees_overall_performance()
    return make_response(performance, 200)


@employees_blueprint.route('/best', methods=['GET'])
def best_performing_employees() -> Response:
    employees = StatisticsService().get_best_or_worst_performing_employees()
    return make_response([employee.to_dict() for employee in employees], 200)


@employees_blueprint.route('/worst', methods=['GET'])
def worst_performing_employees() -> Response:
    employees = StatisticsService().get_best_or_worst_performing_employees(best=False)
    return make_response([employee.to_dict() for employee in employees], 200)


@departments_blueprint.route('/performance', methods=['GET'])
def departments_overall_performance() -> Response:
    performance_scores = StatisticsService().get_department_performance_overview()
    return make_response(performance_scores, 200)


@departments_blueprint.route('/salary', methods=['GET'])
def department_employee_salary_overview() -> Response:
    salaries = StatisticsService().get_department_employee_salary_overview()
    return make_response({department: float(salary) for department, salary in salaries.items()}, 200)


@salaries_blueprint.route('/highest', methods=['GET'])
def employees_with_highest_salary() -> Response:
    employees = StatisticsService().get_employees_with_highest_or_lowest_salary()
    return make_response([employee.to_dict() for employee in employees], 200)


@salaries_blueprint.route('/lowest', methods=['GET'])
def employees_with_lowest_salary() -> Response:
    employees = StatisticsService().get_employees_with_highest_or_lowest_salary(highest=False)
    return make_response([employee.to_dict() for employee in employees], 200)
