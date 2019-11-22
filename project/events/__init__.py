from flask import Flask, render_template, request, flash, redirect, url_for, Blueprint
from flask_login import login_required,logout_user, current_user
from project import app , db
from project.models import User
import requests


event_blueprint = Blueprint('events', __name__ ,template_folder='templates' )


@event_blueprint.route('/home')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    return render_template('views/home.html')