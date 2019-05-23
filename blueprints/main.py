from flask_login import login_required, current_user
from flask import Blueprint, render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from auth.forms import RegistrationForm
from models import db
from models import User, Post, Comment
from flask import Flask
from flask_moment import Moment

app = Flask (__name__)

main = Blueprint('main', __name__)
moment = Moment(app)

@main.route('/index')
@main.route('/')
def index():

    return render_template('index.html')



@main.route('/home')
@login_required
def home():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    comments = Comment.query.order_by(Comment.timestamp.desc()).all()
    
    len_posts = len(posts)
    
    return render_template('home.html', title='Home', comments=comments, posts=posts, len_posts = len_posts, user_id = current_user.id
                                                    , fname=current_user.fname, lname=current_user.lname,username=current_user.username, about_me=current_user.about_me, favecam=current_user.favecam, faveroll = current_user.faveroll, favesubject=current_user.favesubject, instagram_account=current_user.instagram_account)





@main.route('/home', methods=['GET', 'POST'])
@login_required
def home_post():
    post = Post(
                author = current_user ,
                body = request.form.get("userPost") ,
                used_cam = request.form.get('used_cam') ,
                used_roll = request.form.get('used_roll')
                )
    db.session.add(post)
    db.session.commit()

    flash('Your post is now live!')
    return redirect(url_for('main.home'))

@main.route('/comment', methods=['GET', 'POST'])
@login_required
def home_comment():
    comment = Comment(
                post_id = request.form.get("post"),
                commentor = current_user,
                body = request.form.get("body")
                )
    db.session.add(comment)
    db.session.commit()

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


@main.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)

    
    
@main.route('/')
def _view_index():
	if request.args.get('sort') is not None and request.args.get('sort') != '':
		if request.args.get('sort') == 'date':
			posts = Post.query.order_by(Post.post_date.asc()).all()
		if request.args.get('sort') == 'comments':
			posts = Post.query.order_by(Post.post_comment_count.desc()).all()
		if request.args.get('sort') == 'karma':
			posts = Post.query.order_by(Post.post_karma_count.desc()).all()
	else:
		posts = Post.query.order_by(Post.post_date.desc()).all()

	return render_template('index.html', posts=posts)