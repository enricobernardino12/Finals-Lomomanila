from flask import Blueprint, render_template,url_for, redirect, request,flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from auth.forms import RegistrationForm
from models import db
from models import User
from datetime import datetime

authen = Blueprint('authen ', __name__)

@authen.route('/login')
def login():
    return render_template('login.html')

@authen.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # check if meron user na ganon
    user = User.query.filter_by(username=username).first()

    
    # Check password na naka hash
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('authen .login')) # Error if no user or wrong credentials

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

#last seen user
@authen.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@authen.route('/signup')
def signup():
    return render_template('/signup.html')

@authen.route('/signup', methods=['GET', 'POST'])
def signup_post():
    email = request.form.get('email')
    instagram_account = request.form.get('instagram')
    username = request.form.get('username')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('authen .signup'))

    new_user = User(username=username, fname=fname, lname=lname, email=email, instagram_account=instagram_account,password=generate_password_hash(password,method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('authen .login'))



@authen.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))