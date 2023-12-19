from flask import request, Blueprint

from controllers import companies_controller

company = Blueprint('company', __name__)

@company.route('/companies', methods=['GET', 'POST', 'DELETE'])
def companies_controllers():
    if request.method == 'GET':
        return companies_controller.read_companies()
    elif request.method == 'POST':
        return companies_controller.create_company()
    elif request.method == 'DELETE':
        return companies_controller.delete_company()

@company.route('/companies/active', methods=['GET'])
def companies_active_controllers():
    if request.method == 'GET':
        return companies_controller.read_active_companies()
    
@company.route('/companies/<id>', methods=['GET', 'PUT'])
def company_controllers(id):
    if request.method == 'GET':
        return companies_controller.read_company(id)
    elif request.method == 'PUT':
        return companies_controller.update_company(id)
    