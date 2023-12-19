from flask import jsonify, request
from db import db

from models.achievements import Achievements, achievement_schema, achievements_schema
from util.reflection import populate_object

def read_achievements():
    query = db.session.query(Achievements).all()

    if not query:
        return jsonify({"message": "no achievements found"}), 404

    else:
      return jsonify({"message": "achievements found", "results": achievements_schema.dump(query)}), 200

def read_active_achievements():
    query = db.session.query(Achievements).filter(Achievements.active == True).all()

    if not query:
        return jsonify({"message": "no achievements found"}), 404

    else:
      return jsonify({"message": "achievements found", "results": achievements_schema.dump(query)}), 200
    

def read_achievement(id):
    query = db.session.query(Achievements).filter(Achievements.achievement_id == id).first()

    if not query:
        return jsonify({"message": "no achievements found"}), 404

    else:
      return jsonify({"message": "achievement found", "results": achievement_schema.dump(query)}), 200


def create_achievement():
    data = request.form if request.form else request.json

    fields = ['name', 'game_id', 'active']
    required_fields = ['name', 'game_id', 'active']

    values = {}

    for field in fields:
        field_data = data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_achievement = Achievements(values['name'], values['game_id'], values['active'])
    db.session.add(new_achievement)
    db.session.commit()

    return jsonify({"message": "achievement created", "results": achievement_schema.dump(new_achievement)}), 200


def update_achievement(id):
    data = request.form if request.form else request.json
    
    query = db.session.query(Achievements).filter(Achievements.achievement_id == id).first()

    populate_object(query, data)

    db.session.commit()

    return jsonify({"message": "achievement found", "results": achievement_schema.dump(query)}), 200


def delete_achievement():
    data = request.form if request.form else request.json

    fields = ['achievement_id']
    required_fields = ['achievement_id']

    values = {}

    for field in fields:
        field_data = data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400
        
        values[field] = field_data
    
    query = db.session.query(Achievements).filter(Achievements.achievement_id == values['achievement_id']).first()
    if not query:
        return jsonify({"message": "achievement not found"}), 400
    
    db.session.delete(query)
    db.session.commit()

    return jsonify({"message": "achievement deleted", "results": achievement_schema.dump(query)}), 200