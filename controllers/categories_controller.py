from flask import jsonify, request
from db import db

from models.categories import Categories, category_schema, categories_schema
from util.reflection import populate_object

def read_categories():
    query = db.session.query(Categories).all()

    if not query:
        return jsonify({"message": "no categories found"}), 404

    else:
      return jsonify({"message": "categories found", "results": categories_schema.dump(query)}), 200

def read_active_categories():
    query = db.session.query(Categories).filter(Categories.active == True).all()

    if not query:
        return jsonify({"message": "no categories found"}), 404

    else:
      return jsonify({"message": "categories found", "results": categories_schema.dump(query)}), 200
    

def read_category(id):
    query = db.session.query(Categories).filter(Categories.category_id == id).first()

    if not query:
        return jsonify({"message": "no categories found"}), 404

    else:
      return jsonify({"message": "category found", "results": category_schema.dump(query)}), 200


def create_category():
    data = request.form if request.form else request.json

    fields = ['name', 'active']
    required_fields = ['name', 'active']

    values = {}

    for field in fields:
        field_data = data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_category = Categories(values['name'], values['active'])
    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": "category created", "results": category_schema.dump(new_category)}), 200


def update_category(id):
    data = request.form if request.form else request.json
    
    query = db.session.query(Categories).filter(Categories.category_id == id).first()

    populate_object(query, data)

    db.session.commit()

    return jsonify({"message": "category found", "results": category_schema.dump(query)}), 200


def delete_category():
    data = request.form if request.form else request.json

    fields = ['category_id']
    required_fields = ['category_id']

    values = {}

    for field in fields:
        field_data = data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400
        
        values[field] = field_data
    
    query = db.session.query(Categories).filter(Categories.category_id == values['category_id']).first()
    if not query:
        return jsonify({"message": "category not found"}), 400
    
    db.session.delete(query)
    db.session.commit()

    return jsonify({"message": "category deleted", "results": category_schema.dump(query)}), 200