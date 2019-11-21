from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from project import db 



class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(255), nullable = False , unique = True)
    admin = db.Column(db.Boolean, default = False)
    password = db.Column(db.String, nullable = False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


    def generate_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def check_user_email(self, email):
        return User.query.filter_by(email=email).first()



