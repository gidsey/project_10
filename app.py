from flask import Flask, render_template, g, jsonify, flash, redirect, url_for

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from argon2 import PasswordHasher, exceptions

import config
import models
import forms

from auth import auth

from resources.users import users_api
from resources.todos import todos_api

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
HASHER = PasswordHasher()

# Set up the login manager for the app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Name of the login view.


@login_manager.user_loader
def load_user(userid):
    """Look up a user."""
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the DB before each request."""
    g.db = models.db
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the DB connection after each request."""
    g.db.close()
    return response


# Rate limit the APIs
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)
limiter.limit(config.DEFAULT_RATE, per_method=True, methods=["post", "put", "delete"])(todos_api)
limiter.limit("10/day", per_method=True, methods=["post"])(users_api)

# Register the blueprints
app.register_blueprint(users_api, url_prefix='/api/v1')
app.register_blueprint(todos_api, url_prefix='/api/v1')


@app.route('/')
def my_todos():
    return render_template('index.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    """Define the registration view."""
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Registration successful.", "success")
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    """Define the login view."""
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password does not match.", "error")
        else:
            try:
                HASHER.verify(user.password, form.password.data)
            except exceptions.VerifyMismatchError:
                flash("Your email or password does not match.", "error")
            else:
                login_user(user)
                flash("Login successful.", "success")
                return redirect(url_for('my_todos'))
    return render_template('login.html', form=form)  # unsuccessful login


@app.route('/logout')
@login_required
def logout():
    """Define the logout view."""
    logout_user()
    flash("Logout successful.", "success")
    return redirect(url_for('my_todos'))


@app.route('/api/v1/users/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
