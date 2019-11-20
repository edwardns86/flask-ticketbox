from flask import Blueprint, render_template


event_blueprint = Blueprint('events', __name__ ,template_folder='templates' )

@event_blueprint.route('/')
def root():
    return render_template('events/index.html')