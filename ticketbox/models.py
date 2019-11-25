from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ticketbox import db 
from datetime import datetime




class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(255), nullable = False , unique = True)
    admin = db.Column(db.Boolean, default = False)
    organiser = db.Column(db.Boolean, default = False)
    password = db.Column(db.String, nullable = False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    events = db.relationship("Event", backref='user', lazy=True)
    orders = db.relationship("Order", backref='user', lazy=True)
    def generate_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def check_user_email(self, email):
        return User.query.filter_by(email=email).first()

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable = False)
    content = db.Column(db.String, nullable=False)
    banner_url = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    event_start_date = db.Column(db.DateTime, nullable=False, default=datetime.date)
    # event_start_time = db.Column(db.String, nullable=False )
    event_end_date = db.Column(db.DateTime ,nullable=False , default=datetime.date)
    # event_end_time = db.Column(db.String ,nullable=False )
    organiser_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tickets = db.relationship("Ticket", backref="event" , lazy=True)
    

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    ticket_type = db.Column(db.String, nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    ticket_qty = db.Column(db.Integer, nullable=False)
    orders = db.relationship("Event", backref='user', lazy=True)
    # HERE IS WHERE I AM AT THE LAST CHANGE 

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    completed = db.Column(db.Boolean, default=False)
    items = db.relationship("OrderItem", backref='order', lazy=True )

class OrderItem(db.Model):
    __tablename__ = 'orderitems'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
   
   
   
   
   
   
    # add tags later

# class Tag(db.Model):
#     __tablename__ = 'tags'
#     id = db.Column(db.Integer, primary_key=True)
#     category = db.Column(db.String(35))

# class Order(db.Model):
#     __tablename__ = 'orders'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id


# class OrderItem(db.Model):
#     __tablename__ = 'orderitems'
#     id = db.Column(db.Integer, primary_key=True)
#     order_id




