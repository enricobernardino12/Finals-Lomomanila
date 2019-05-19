from flask_login import login_required, current_user
from flask import Blueprint, render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from auth.forms import RegistrationForm
from models import db
from models import User, Post

main = Blueprint('main', __name__)

@main.route('/index')
@main.route('/')
def index():

    return render_template('index.html')


@main.route('/home')
@login_required
def home():
    
    return render_template('home.html', post=current_user.post)

@main.route('/home', methods=['GET', 'POST'])
@login_required
def home_post():

    body = request.form.get('post')

    post = Post(body= body , author = current_user)
    db.session.add(post)
    db.session.commit()

    flash('Your post is now live!')
    return redirect(url_for('main.home'))



@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', fname=current_user.fname, email=current_user.email, lname=current_user.lname, username=current_user.username, about_me=current_user.about_me, favecam=current_user.favecam, faveroll = current_user.faveroll, favesubject=current_user.favesubject, instagram_account = current_user.instagram_account)

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

#Profile Posts

# @main.route('/user/<username>')
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     page = request.args.get('page', 1, type=int)
#     posts = user.posts.order_by(Post.timestamp.desc()).paginate(
#         page, app.config['POSTS_PER_PAGE'], False)
#     next_url = url_for('user', username=user.username, page=posts.next_num) \
#         if posts.has_next else None
#     prev_url = url_for('user', username=user.username, page=posts.prev_num) \
#         if posts.has_prev else None
#     return render_template('user.html', user=user, posts=posts.items,
#                            next_url=next_url, prev_url=prev_url)
