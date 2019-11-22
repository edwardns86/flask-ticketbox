from flask import Flask, render_template, redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user


app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

from project.models import User
login_manager = LoginManager(app)
migrate=Migrate(app, db)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

from project.users import user_blueprint
app.register_blueprint(user_blueprint, url_prefix = '/user')

from project.events import event_blueprint
app.register_blueprint(event_blueprint, url_prefix = '/event')

@app.route('/')
def root():
    if current_user.is_authenticated:
        return redirect(url_for('events.root'))
    return redirect(url_for('users.register'))  