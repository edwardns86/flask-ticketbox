from flask import Blueprint, render_template


user_blueprint = Blueprint('users', __name__ ,template_folder='templates' )

@user_blueprint.route('/')
def root():
    return render_template('users/index.html')