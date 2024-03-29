from flask import Flask, render_template, redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
import config

app = Flask(__name__)

app.config.from_object(config.Config)

db = SQLAlchemy(app)

from ticketbox.models import User , Ticket , Event , Order
login_manager = LoginManager(app)
migrate=Migrate(app, db)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

from ticketbox.users import user_blueprint
app.register_blueprint(user_blueprint, url_prefix = '/user')

from ticketbox.profiles import profile_blueprint
app.register_blueprint(profile_blueprint, url_prefix = '/profile')

from ticketbox.events import event_blueprint
app.register_blueprint(event_blueprint, url_prefix = '/event')

from ticketbox.tickets import ticket_blueprint
app.register_blueprint(ticket_blueprint, url_prefix = '/ticket')

@app.route('/')
def root():
    if current_user.is_authenticated:
        return redirect(url_for('events.home'))
    return redirect(url_for('users.register'))  