from flask import Flask, render_template, request, flash, redirect, url_for, Blueprint
from flask_login import login_required,logout_user, current_user
from ticketbox import app , db
from ticketbox.models import User , Event , Ticket , Order , OrderItem
from datetime import datetime
import requests

profile_blueprint = Blueprint('profiles', __name__ ,template_folder='templates' )


@profile_blueprint.route('/orders')
def order_history():
    order = Order.query.filter_by(user_id = current_user.id)
    order.items = []
    for item in order.items:
        order.items.append(Ticket.query.get(item.ticket_id))
    return render_template('views/profile.html')
    