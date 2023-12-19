import uuid
import marshmallow as ma

from db import db

users_achievements_association_table = db.Table(
    "UsersAchievementsAssociation",
    db.Model.metadata,
    db.Column('user_id', db.ForeignKey('Users.user_id'), primary_key=True),
    db.Column('achievement_id', db.ForeignKey('Achievements.achievement_id'), primary_key=True)
)