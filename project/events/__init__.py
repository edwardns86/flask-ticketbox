from flask import Blueprint, render_template


event_blueprint = Blueprint('events', __name__ ,template_folder='templates' )


@event_blueprint.route('/home')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    return render_template('views/home.html')