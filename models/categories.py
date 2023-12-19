import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

from models.games_categories_xref import games_categories_association_table

class Categories(db.Model):
    __tablename__ = "Categories"

    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False, unique=True)
    active = db.Column(db.Boolean(), default=True)

    games = db.relationship("Games", secondary=games_categories_association_table, back_populates='categories')

    def __init__(self, name, active):
        self.name = name
        self.active = active

class CategoriesSchema(ma.Schema):
    class Meta:
        fields = ['category_id', 'name', 'games', 'active']

    games = ma.fields.Nested("GamesSchema", many=True, exclude=['categories'])

category_schema = CategoriesSchema()
categories_schema = CategoriesSchema(many=True)