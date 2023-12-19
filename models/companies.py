import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

class Companies(db.Model):
    __tablename__ = "Companies"

    company_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False, unique=True)
    active = db.Column(db.Boolean(), default=True)

    games = db.relationship("Games", foreign_keys='[Games.company_id]', back_populates='company')

    def __init__(self, name, active):
        self.name = name
        self.active = active

class CompaniesSchema(ma.Schema):
    class Meta:
        fields = ['company_id', 'name', 'active']

company_schema = CompaniesSchema()
companies_schema = CompaniesSchema(many=True)