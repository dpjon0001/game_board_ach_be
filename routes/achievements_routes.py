from flask import request, Blueprint

from controllers import achievements_controller

achievement = Blueprint('achievement', __name__)

@achievement.route('/achievements', methods=['GET', 'POST', 'DELETE'])
def achievements_controllers():
    if request.method == 'GET':
        return achievements_controller.read_achievements()
    elif request.method == 'POST':
        return achievements_controller.create_achievement()
    elif request.method == 'DELETE':
        return achievements_controller.delete_achievement()

@achievement.route('/achievements/active', methods=['GET'])
def achievements_active_controllers():
    if request.method == 'GET':
        return achievements_controller.read_active_achievements()
    
@achievement.route('/achievements/<id>', methods=['GET', 'PUT'])
def achievement_controllers(id):
    if request.method == 'GET':
        return achievements_controller.read_achievement(id)
    elif request.method == 'PUT':
        return achievements_controller.update_achievement(id)