from flask import jsonify, request
from db import db

from models.users import Users, user_schema, users_schema
from models.achievements import Achievements
from util.reflection import populate_object

def read_users():
    query = db.session.query(Users).all()

    if not query:
        return jsonify({"message": "no users found"}), 404

    else:
      return jsonify({"message": "users found", "results": users_schema.dump(query)}), 200

def read_active_users():
    query = db.session.query(Users).filter(Users.active == True).all()

    if not query:
        return jsonify({"message": "no users found"}), 404

    else:
      return jsonify({"message": "users found", "results": users_schema.dump(query)}), 200
    

def read_user(id):
    query = db.session.query(Users).filter(Users.user_id == id).first()

    if not query:
        return jsonify({"message": "no users found"}), 404

    else:
      return jsonify({"message": "user found", "results": user_schema.dump(query)}), 200


def create_user():
    data = request.form if request.form else request.json

    fields = ['username', 'email', 'password', 'role', 'active']
    required_fields = ['username', 'email', 'password', 'role', 'active']

    values = {}

    for field in fields:
        field_data = data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_user = Users(values['username'], values['email'], values['password'], values['role'], values['active'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "user created", "results": user_schema.dump(new_user)}), 200


def update_user(id):
    data = request.form if request.form else request.json
    
    query = db.session.query(Users).filter(Users.user_id == id).first()

    populate_object(query, data)

    db.session.commit()

    return jsonify({"message": "user found", "results": user_schema.dump(query)}), 200


def delete_user():
    data = request.form if request.form else request.json

    fields = ['user_id']
    required_fields = ['user_id']

    values = {}

    for field in fields:
        field_data = data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400
        
        values[field] = field_data
    
    query = db.session.query(Users).filter(Users.user_id == values['user_id']).first()
    if not query:
        return jsonify({"message": "user not found"}), 400
    
    db.session.delete(query)
    db.session.commit()

    return jsonify({"message": "user deleted", "results": user_schema.dump(query)}), 200

def create_user_achievement():
    data = request.form if request.form else request.json
    user_id = data.get("user_id")
    achievement_id = data.get("achievement_id")

    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()
    achievement_query = db.session.query(Achievements).filter(Achievements.achievement_id == achievement_id).first()

    user_query.achievements.append(achievement_query)

    db.session.commit()

    return jsonify({"message": "Achievement added to user", "user": user_schema.dump(user_query)}), 200