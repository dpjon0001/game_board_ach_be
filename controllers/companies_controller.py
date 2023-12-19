from flask import jsonify, request
from db import db

from models.companies import Companies, company_schema, companies_schema
from util.reflection import populate_object

def read_companies():
    query = db.session.query(Companies).all()

    if not query:
        return jsonify({"message": "no companies found"}), 404

    else:
      return jsonify({"message": "companies found", "results": companies_schema.dump(query)}), 200

def read_active_companies():
    query = db.session.query(Companies).filter(Companies.active == True).all()

    if not query:
        return jsonify({"message": "no companies found"}), 404

    else:
      return jsonify({"message": "companies found", "results": companies_schema.dump(query)}), 200
    

def read_company(id):
    query = db.session.query(Companies).filter(Companies.company_id == id).first()

    if not query:
        return jsonify({"message": "no companies found"}), 404

    else:
      return jsonify({"message": "company found", "results": company_schema.dump(query)}), 200


def create_company():
    data = request.form if request.form else request.json

    fields = ['name', 'active']
    required_fields = ['name', 'active']

    values = {}

    for field in fields:
        field_data = data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_company = Companies(values['name'], values['active'])
    db.session.add(new_company)
    db.session.commit()

    return jsonify({"message": "company created", "results": company_schema.dump(new_company)}), 200


def update_company(id):
    data = request.form if request.form else request.json
    
    query = db.session.query(Companies).filter(Companies.company_id == id).first()

    populate_object(query, data)

    db.session.commit()

    return jsonify({"message": "company found", "results": company_schema.dump(query)}), 200


def delete_company():
    data = request.form if request.form else request.json

    fields = ['company_id']
    required_fields = ['company_id']

    values = {}

    for field in fields:
        field_data = data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400
        
        values[field] = field_data
    
    query = db.session.query(Companies).filter(Companies.company_id == values['company_id']).first()
    if not query:
        return jsonify({"message": "company not found"}), 400
    
    db.session.delete(query)
    db.session.commit()

    return jsonify({"message": "company deleted", "results": company_schema.dump(query)}), 200