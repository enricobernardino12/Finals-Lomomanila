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



# @app.route('/login', methods=['POST', 'GET'])
# def loginForm():

#     if request.method == 'GET' :
#         return render_template('login.html', value=0)
#     elif request.method == 'POST' :
#         session['username'] = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=session['username'], pword=password).first() #filter results ; .all() -return all tasks
#         if not user:
#             session.clear()
#             return render_template('login.html', test=2, value=0)
#         return redirect(url_for('home'))
#     return render_template('login.html', value=0)


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm(request.form)
#     if request.method == 'POST' and form.validate():
#         users = user(username=form.username.data, email = form.email.data, instagram_account = form.instagram_account.data, password = form.password.data)
#         db.session.add(users)
#         db.session.commit()
#         flash('Thanks for registering')
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)

# @app.route('/test-connection')
# def hello():
#     try:
#         db.session.query('1').all()
#         return 'Connected.'
#     except Exception as e:
#         return str(e)



# UPDATE #

#For login


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
