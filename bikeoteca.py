from flask import Flask
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = MySQL(app)
from views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)