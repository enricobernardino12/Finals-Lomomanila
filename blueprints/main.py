from flask_login import login_required, current_user
from flask import Blueprint, render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from auth.forms import RegistrationForm
from models import db
from models import User
from models import Post

main = Blueprint('main', __name__)

@main.route('/index')
@main.route('/')
def index():

    return render_template('index.html')

@main.route('/home')
@login_required
def home():
    return render_template('home.html')

@main.route('/home', methods=['GET', 'POST'])
@login_required
def home_post():

    body = request.form.get('post')
    author = current_user.username

    post = Post(body= body)
    db.session.add(post)
    db.session.commit()

    flash('Your post is now live!')
    return redirect(url_for('main.home'))



@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', fname=current_user.fname, lname=current_user.lname,username=current_user.username, about_me=current_user.about_me, favecam=current_user.favecam, faveroll = current_user.faveroll, favesubject=current_user.favesubject, instagram_account=current_user.instagram_account)

#create schema db
@main.route('/create-schema')
def create_schema():
    db.create_all()
    return 'Schema created.'

@main.route('/editprofile')
@login_required
def editprofile():
    return render_template('/editprofile.html', fname=current_user.fname, lname=current_user.lname,username=current_user.username, about_me=current_user.about_me, favecam=current_user.favecam, faveroll = current_user.faveroll, favesubject=current_user.favesubject, instagram_account=current_user.instagram_account)

@main.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editprofile_post():
    current_user.about_me = request.form.get('about_me')
    current_user.favecam = request.form.get('favecam')
    current_user.faveroll = request.form.get('faveroll')
    current_user.favesubject = request.form.get('favesubj')
    current_user.instagram_accout = request.form.get('instagram_account')
    db.session.commit()
    flash('Your changes have been saved.')
    return redirect(url_for('main.profile'))

