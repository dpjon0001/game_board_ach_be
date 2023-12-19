from flask import Flask, jsonify, request
import psycopg2
import os
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from db import *

from routes.users_routes import user
from routes.companies_routes import company
from routes.categories_routes import category
from routes.games_routes import game
from routes.achievements_routes import achievement

from models.achievements import Achievements, achievement_schema, achievements_schema
from models.categories import Categories, category_schema, categories_schema
from models.companies import Companies, company_schema, companies_schema
from models.games import Games, game_schema, games_schema
from models.users import Users, user_schema, users_schema

flask_host = os.environ.get("FLASK_HOST")
flask_port = os.environ.get("FLASK_PORT")

database_scheme = os.environ.get("DATABASE_SCHEME")
database_user = os.environ.get("DATABASE_USER")
database_address = os.environ.get("DATABASE_ADDRESS")
database_password = os.environ.get("DATABASE_PASSWORD")
database_port = os.environ.get("DATABASE_PORT")
database_name = os.environ.get("DATABASE_NAME")

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = f"{database_scheme}{database_user}:{database_password}@{database_address}:{database_port}/{database_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app, db)
ma = Marshmallow(app)
app.register_blueprint(user)
app.register_blueprint(company)
app.register_blueprint(category)
app.register_blueprint(game)
app.register_blueprint(achievement)

def create_tables():
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables created")

create_tables()

if __name__ == '__main__':
    app.run(host=flask_host, port=flask_port)