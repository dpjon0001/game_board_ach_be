import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from models.games import Games, GamesSchema
from models.users_achievements_xref import users_achievements_association_table

class Achievements(db.Model):
    __tablename__ = "Achievements"

    achievement_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False, unique=True)
    game_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Games.game_id"), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    game = db.relationship("Games", foreign_keys='[Achievements.game_id]', back_populates='achievements')

    users = db.relationship("Users", secondary=users_achievements_association_table, back_populates="achievements")

    def __init__(self, name, game_id, active):
        self.name = name
        self.game_id = game_id
        self.active = active

class AchievementsSchema(ma.Schema):
    class Meta:
        fields = ['achievement_id', 'name', 'game', 'users', 'active']
        
    game = ma.fields.Nested("GamesSchema")
    users = ma.fields.Nested("UsersSchema", many=True, exclude=['achievements'])

achievement_schema = AchievementsSchema()
achievements_schema = AchievementsSchema(many=True)