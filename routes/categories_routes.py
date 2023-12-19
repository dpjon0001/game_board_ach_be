from flask import request, Blueprint

from controllers import categories_controller

category = Blueprint('category', __name__)

@category.route('/categories', methods=['GET', 'POST', 'DELETE'])
def categories_controllers():
    if request.method == 'GET':
        return categories_controller.read_categories()
    elif request.method == 'POST':
        return categories_controller.create_category()
    elif request.method == 'DELETE':
        return categories_controller.delete_category()

@category.route('/categories/active', methods=['GET'])
def categories_active_controllers():
    if request.method == 'GET':
        return categories_controller.read_active_categories()
    
@category.route('/categories/<id>', methods=['GET', 'PUT'])
def category_controllers(id):
    if request.method == 'GET':
        return categories_controller.read_category(id)
    elif request.method == 'PUT':
        return categories_controller.update_category(id)