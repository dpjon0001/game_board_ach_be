from flask import request, Blueprint

from controllers import games_controller

game = Blueprint('game', __name__)

@game.route('/games', methods=['GET', 'POST', 'DELETE'])
def games_controllers():
    if request.method == 'GET':
        return games_controller.read_games()
    elif request.method == 'POST':
        return games_controller.create_game()
    elif request.method == 'DELETE':
        return games_controller.delete_game()

@game.route('/games/active', methods=['GET'])
def games_active_controllers():
    if request.method == 'GET':
        return games_controller.read_active_games()
    
@game.route('/games/<id>', methods=['GET', 'PUT'])
def game_controllers(id):
    if request.method == 'GET':
        return games_controller.read_game(id)
    elif request.method == 'PUT':
        return games_controller.update_game(id)
    
@game.route('/games/categories', methods=['POST'])
def game_categories_controllers():
    if request.method == 'POST':
        return games_controller.create_game_category()