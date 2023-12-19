import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from models.companies import Companies, CompaniesSchema
from models.games_categories_xref import games_categories_association_table

class Games(db.Model):
    __tablename__ = "Games"

    game_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False, unique=True)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Companies.company_id"), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    achievements = db.relationship("Achievements", foreign_keys='[Achievements.game_id]', back_populates='game')
    company = db.relationship("Companies", foreign_keys='[Games.company_id]', back_populates='games')
    categories = db.relationship("Categories", secondary=games_categories_association_table, back_populates='games')

    def __init__(self, name, company_id, category_id, active):
        self.name = name
        self.company_id = company_id
        self.active = active

class GamesSchema(ma.Schema):
    class Meta:
        fields = ['game_id', 'name', 'company', 'categories', 'active']

    company = ma.fields.Nested("CompaniesSchema")   
    categories = ma.fields.Nested("CategoriesSchema", many=True, exclude=['games'])      

game_schema = GamesSchema()
games_schema = GamesSchema(many=True)