from flask import (Flask)


import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
