from flask_login import UserMixin
from project import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default = False)