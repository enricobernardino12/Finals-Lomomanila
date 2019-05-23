from flask import Flask, render_template, request, session, redirect, url_for, make_response, flash, abort
# from auth.forms import RegistrationForm
from models import db


import os


from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db=SQLAlchemy()

app = Flask (__name__)
#secret key
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:secret@database/testdatabase'
                                        #<dialect+driver>://<username>:<password>@ghost/<database>
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'authen .login'
login_manager.init_app(app)





from models import User

#Creates cookie and searches it in db from id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




#auth is for login sign 
from blueprints.authen import authen as authen_blueprint
app.register_blueprint(authen_blueprint)

#main will be index and profile
from blueprints.main import main as main_blueprint
app.register_blueprint(main_blueprint)

#Mail part

# from flask import Flask
# from flask_mail import Mail
# from flask_mail import Message
# from app import mail

# app = Flask(__name__)
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'alee.policarpio@iacademy.edu.ph'
# app.config['MAIL_PASSWORD'] = 'password'
# app.config['MAIL_DEFAULT_SENDER'] = 'alee.policarpio@iacademy.edu.ph'
# mail = Mail(app)


# def send_email(subject, sender, recipients, text_body, html_body):
#     msg = Message(subject, sender=sender, recipients=recipients)
#     msg.body = text_body
#     msg.html = html_body
#     mail.send(msg)

# from email import send_email
# @app.route('/signup', methods=['POST'])
# def signup():
#     user = User(name=request.form.get('name'), password=request.form.get('password'), email=request.form.get('email'))
#     db.session.add(user)
#     db.session.commit()
#     message = 'Welcome to my forum'
#     send_email('Welcome', 'alee.policarpio@iacademy.edu.ph', [email=user.email], message, message)
#     return render_template('home.html', user=user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
