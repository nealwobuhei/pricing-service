from flask import request, Blueprint, render_template, session, url_for, redirect

from models.user import User, UserErrors

user_blueprint = Blueprint('users', __name__)

"""
cookie: pieces of data that are stored on the browser. and alongside data we store what web-page sets the cookie
session: piece of data that is stored inside our application and stored for each user differently
each user has individual session
when we get those cookies, Flask will tell us the session that is associated to it
when browser send us cookie, Flask let the session which is for this user, we can store whatever we want in that session
when cookie is received by our app, Flask will populate the session with the data that we've set earlier on

session related to specific user, since browser will send us a cookie, a piece of data that tell us which session
that browser is related to, so when user login, that cookie will be related to specific session which contain their email
"""


# create structure of endpoint
@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            User.register_user(email, password)
            session['email'] = email  # once we register the user, store the users email inside the session(like Dict)
            return email

        except UserErrors.UserError as e:
            return e.message  # access the message property of e

    return render_template('users/register.html')


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email  # only way the session could have an email is if they logged in or registered
                return email

        except UserErrors.UserError as e:
            return e.message

    return render_template('users/login.html')


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect('.user_login')