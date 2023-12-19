from flask import request, Blueprint

from controllers import users_controller

user = Blueprint('user', __name__)

@user.route('/users', methods=['GET', 'POST', 'DELETE'])
def users_controllers():
    if request.method == 'GET':
        return users_controller.read_users()
    elif request.method == 'POST':
        return users_controller.create_user()
    elif request.method == 'DELETE':
        return users_controller.delete_user()

@user.route('/users/active', methods=['GET'])
def users_active_controllers():
    if request.method == 'GET':
        return users_controller.read_active_users()
    
@user.route('/users/<id>', methods=['GET', 'PUT'])
def user_controllers(id):
    if request.method == 'GET':
        return users_controller.read_user(id)
    elif request.method == 'PUT':
        return users_controller.update_user(id)
    
@user.route('/users/achievements', methods=['POST'])
def user_achievement_controllers():
    if request.method == 'POST':
        return users_controller.create_user_achievement()