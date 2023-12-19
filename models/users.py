import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

from models.users_achievements_xref import users_achievements_association_table

class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    achievements = db.relationship("Achievements", secondary=users_achievements_association_table, back_populates="users")

    def __init__(self, username, email, password, role, active):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.active = active

class UsersSchema(ma.Schema):
    class Meta:
        fields = ['user_id', 'username', 'email', 'password', 'role', 'achievements', 'active']

    achievements = ma.fields.Nested("AchievementsSchema", many=True, exclude=['users'])

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)