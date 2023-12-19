import uuid
import marshmallow as ma

from db import db

games_categories_association_table = db.Table(
    "GamesCategoriesAssociation",
    db.Model.metadata,
    db.Column('game_id', db.ForeignKey('Games.game_id'), primary_key=True),
    db.Column('category_id', db.ForeignKey('Categories.category_id'), primary_key=True)
)