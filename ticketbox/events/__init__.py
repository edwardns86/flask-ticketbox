from flask import Flask, render_template, request, flash, redirect, url_for, Blueprint
from flask_login import login_required,logout_user, current_user
from ticketbox import app , db
from ticketbox.models import User , Event , Ticket
from datetime import datetime
import requests


event_blueprint = Blueprint('events', __name__ ,template_folder='templates' )
@event_blueprint.route('/home')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    events = Event.query.all()
    return render_template('views/home.html', events=events)

@event_blueprint.route('/create-event', methods = ['GET', 'POST'])
@login_required
def create_event():
    if request.method == "POST":
        new_event=Event(
            title = request.form['title'],
            content = request.form['content'],
            banner_url = request.form['banner_url'],
            location = request.form['location'],
            event_start_date = request.form['event_start_date'],
            # event_start_time = request.form['event_start_time'],
            event_end_date = request.form['event_end_date'],
            # event_end_time = request.form['event_end_time'],
            organiser_id = current_user.id
        )
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('events.view_event', id=new_event.id))
    return render_template('views/create-event.html')


@event_blueprint.route('/viewevent/<id>', methods = ['GET', 'POST'])
@login_required
def view_event(id):
    event = Event.query.get(id)
    return render_template('views/event-view.html', event = event , id=id)

@event_blueprint.route('/<int:id>/add-tickets',  methods = ['GET', 'POST'])
@login_required

def add_event_tickets(id):
    event = Event.query.get(id)
    if request.method == 'POST':
        new_ticket = Ticket(
            event_id = id,
            ticket_type = request.form['ticket_type'],
            ticket_price = request.form['ticket_price'],
            ticket_qty = request.form['ticket_qty']
        )
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for('events.add_event_tickets', event= event , id=id))
    return render_template('views/add-tickets.html', event=event ,id=id )