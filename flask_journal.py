from flask import (Flask, render_template, redirect, url_for, g, flash)
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import (LoginManager, current_user, login_user,
                             logout_user, login_required)


import forms
import models


DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'sldfjlkj(*SD^&(*&(ohjlk3298yukjsdhfk)))'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    """This finds a user or returns None."""
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Closes the database connection after each request."""
    g.db.close()
    return response


@app.route('/')
def index():
    """This is the homepage for the Flask Learning Journal"""
    return render_template('index.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    """This is the new user registation page."""
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("You are registered!", "success")
        models.User.create_user(
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    """Allows the user to log in."""
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email does not exist :{")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Welcome to your Journal!", "success")
                return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """Allows the user to log out."""
    logout_user()
    flash("Until next time, fairwell.")
    return redirect(url_for('index'))


@app.route('/new.html', methods=('GET', 'POST'))
def new():
    """This lets the user create a new Entry."""
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.create(user=g.user.id,
                            title=form.title.data,
                            entry_date=form.entry_date.data,
                            time_spent=form.time_spent.data,
                            learned=form.learned.data,
                            resources=form.resources.data
                            )
        flash("Your Journal entry has been created.", "success")
        # temporary placeholder change index for /details
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/detail.html')
def detail():
    """This lets a user closely examine an Entry."""
    return render_template('detail.html')


@app.route('/edit.html')
def edit():
    """This is where the user can edit an Entry."""
    return render_template('edit.html')


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            email="example@example.com",
            password="password",
            admin=True
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
