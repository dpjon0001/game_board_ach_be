from flask import jsonify, request
from db import db

from models.games import Games, game_schema, games_schema
from models.categories import Categories
from util.reflection import populate_object

def read_games():
    query = db.session.query(Games).all()

    if not query:
        return jsonify({"message": "no games found"}), 404

    else:
      return jsonify({"message": "games found", "results": games_schema.dump(query)}), 200

def read_active_games():
    query = db.session.query(Games).filter(Games.active == True).all()

    if not query:
        return jsonify({"message": "no games found"}), 404

    else:
      return jsonify({"message": "games found", "results": games_schema.dump(query)}), 200
    

def read_game(id):
    query = db.session.query(Games).filter(Games.game_id == id).first()

    if not query:
        return jsonify({"message": "no games found"}), 404

    else:
      return jsonify({"message": "game found", "results": game_schema.dump(query)}), 200


def create_game():
    data = request.form if request.form else request.json

    fields = ['name', 'company_id', 'category_id', 'active']
    required_fields = ['name', 'company_id', 'category_id', 'active']

    values = {}

    for field in fields:
        field_data = data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_game = Games(values['name'], values['company_id'], values['category_id'], values['active'])
    db.session.add(new_game)
    db.session.commit()

    return jsonify({"message": "game created", "results": game_schema.dump(new_game)}), 200


def update_game(id):
    data = request.form if request.form else request.json
    
    query = db.session.query(Games).filter(Games.game_id == id).first()

    populate_object(query, data)

    db.session.commit()

    return jsonify({"message": "game found", "results": game_schema.dump(query)}), 200


def delete_game():
    data = request.form if request.form else request.json

    fields = ['game_id']
    required_fields = ['game_id']

    values = {}

    for field in fields:
        field_data = data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400
        
        values[field] = field_data
    
    query = db.session.query(Games).filter(Games.game_id == values['game_id']).first()
    if not query:
        return jsonify({"message": "game not found"}), 400
    
    db.session.delete(query)
    db.session.commit()

    return jsonify({"message": "game deleted", "results": game_schema.dump(query)}), 200

def create_game_category():
    data = request.form if request.form else request.json
    game_id = data.get("game_id")
    category_id = data.get("category_id")

    game_query = db.session.query(Games).filter(Games.game_id == game_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    game_query.categories.append(category_query)

    db.session.commit()

    return jsonify({"message": "category added to game", "game": game_schema.dump(game_query)}), 200