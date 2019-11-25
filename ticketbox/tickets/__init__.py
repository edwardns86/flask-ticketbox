from flask import Flask, render_template, request, flash, redirect, url_for, Blueprint
from flask_login import login_required,logout_user, current_user
from ticketbox import app , db
from ticketbox.models import  Event , Ticket , Order , OrderItem
from datetime import datetime
import requests

ticket_blueprint = Blueprint('tickets', __name__ ,template_folder='templates' )


@ticket_blueprint.route('/<int:id>/add-tickets',  methods = ['GET', 'POST'])
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
        return redirect(url_for('tickets.add_event_tickets', event= event , id=id))
    return render_template('views/add-tickets.html', event=event ,id=id )

@ticket_blueprint.route('/purchase', methods = ['GET', 'POST'] )
def purchase():
    
    if request.method == 'POST':
        order = Order( 
        user_id=current_user.id, 
        completed=True)
        db.session.add(order)
        db.session.commit()
        event = Event.query.get(request.form['event_id'])
        for ticket in event.tickets():
            selected_ticket = request.form['ticket_id_{0}'.format(ticket.id)] 
            selected_ticket_quantity = request.form['ticket_qty_{0}'.format(ticket.id)]
            if selected_ticket and int(selected_ticket_quantity) > 0:
                numberrrr = int(request.form['ticket_qty_{0}'.format(ticket.id)])
                for number in range(0, numberrrr):
                    order_item = OrderItem(order_id=order.id, ticket_id=ticket.id)
                    ticket.ticket_qty -= 1
                    db.session.add(order_item)
                    db.session.commit()
                ticket.ticket_qty -= numberrrr
    return redirect(url_for('events.home'))