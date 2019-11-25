from flask import Flask, render_template, request, flash, redirect, url_for, Blueprint
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ticketbox import app , db
from ticketbox.models import User, Event, Ticket
from itsdangerous import URLSafeTimedSerializer
import requests

user_blueprint = Blueprint('users', __name__ ,template_folder='templates' )

def send_reset_email(name, email, token):
    url = "https://api.mailgun.net/v3/sandboxa6490de950964fd4aa2a67bf3143af71.mailgun.org/messages"
    try:    
        response = requests.post(url, 
                                auth=("api", app.config['MAILGUN_API']), 
                                data={"from": "Edward : <edwardns86@gmail.com>",
                                "to": [email], 
                                "subject": "Reset Password", 
                                "text":f"Hi {name} please click on this link to reset your password http://localhost:5000/user/new-password/{token}"}
                                )
        response.raise_for_status()
    except Exception as err:
        print(f'Other error occurred: {err}')  
    else:
        print('Success!')

@user_blueprint.route('/')
def root():
    return render_template('users/index.html')

@user_blueprint.route('/login',methods=[ 'GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('events.home'))
    if request.method == "POST":
        user = User(email = request.form["email"]).check_user_email(request.form["email"])
        if not user: 
            flash("Your email is not registered",'warning')
            return redirect(url_for('users.register'))
        if user.check_password(request.form["password"]):   
            login_user(user)
            flash("Welcome back!", "success")
            return redirect(url_for('events.home'))
        flash('Incorrect password, please try to login again', 'warning')
    return render_template("views/login.html")    

@user_blueprint.route('/logout', methods=[ 'GET', 'POST'])
@login_required  
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@user_blueprint.route('/register', methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('events.home'))
    if request.method == 'POST':  
        check_email = User.query.filter_by(email=request.form['email']).first() 
        if check_email:  
            flash('Email already taken', 'warning')
            return redirect(url_for('users.login')) 
        if request.form['password'] != request.form['checkpassword']:
            flash('The passwords entered do not match', 'warning')
            return redirect(url_for('users.register'))
        new_user = User(name=request.form['name'],  
                        email=request.form['email'],
                        )
        new_user.generate_password(request.form['password'])  
        db.session.add(new_user) 
        db.session.commit() 
        login_user(new_user) 
        flash('Successfully created an account and logged in', 'success')
        return redirect(url_for('events.home')) # and redirect user to our root
    return render_template('views/register.html') 

@user_blueprint.route('/forgotten-password', methods=[ 'GET', 'POST'])

def forgotten_password():
    if request.method == 'POST':
        user = User(email = request.form["email"]).check_user_email()
        if not user:
            flash('We do not have this email address in our system', 'warning')
            return redirect(url_for('users.forgotten_password'))
        s = URLSafeTimedSerializer(app.secret_key)
        token = s.dumps(user.email, salt="RESET_PASSWORD")
        send_reset_email(user.name, user.email, token)
        flash('We have sent an email to your account with a link to reset your password. Please check your spam if you cannot see it.', 'success')
        return redirect(url_for('users.login'))
    return render_template('views/request-password.html')


@user_blueprint.route('/new-password/<token>', methods= [ 'GET', 'POST'])
def set_new_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('events.home'))
    
    s = URLSafeTimedSerializer(app.secret_key)
    email = s.loads(token , salt="RESET_PASSWORD", max_age=10000)
    user = User(email = email).check_user_email(email)
    if not user:
        flash("no user")
        return redirect(url_for('users.forgotten_password'))
    if request.method == 'POST':
        if request.form['password'] != request.form['checkpassword']:
            flash('passwords do not match')
            return redirect(url_for('users.set_new_password', token=token))
        user.generate_password(request.form['password'])
        db.session.commit()
        flash('We have set a new password for you...')
        return redirect(url_for('users.login'))
    return render_template('views/password-reset.html', token=token)  