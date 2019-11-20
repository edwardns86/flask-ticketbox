from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate




app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

from project.models import User
migrate=Migrate(app, db)


from project.users import user_blueprint
app.register_blueprint(user_blueprint, url_prefix = '/user')

from project.events import event_blueprint
app.register_blueprint(event_blueprint, url_prefix = '/event')


@app.route('/')
def root():
    return 'Home Page'