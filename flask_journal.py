from flask import (Flask, render_template, redirect, url_for)


DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)


@app.route('/')
def index():
    """This is the homepage for the Flask Learning Journal"""
    # current_user is a temporary place holder for loggin in.
    # That is until I add a way for users to log in.
    return render_template('index.html', current_user=False)


@app.route('/login')
def login():
    """Allows the user to log in."""
    # temporary placeholder
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    """Allows the user to log out."""
    # temporary placeholder
    return redirect(url_for('index'))


@app.route('/new.html')
def new():
    """This lets the user create a new Entry."""
    return render_template('new.html', current_user=True)


@app.route('/detail.html')
def detail():
    """This lets a user closely examine an Entry."""
    return render_template('detail.html', current_user=False)


@app.route('/edit.html')
def edit():
    """This is where the user can edit an Entry."""
    return render_template('edit.html', current_user=True)


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
