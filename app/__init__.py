from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


import time
from flask import g

app = Flask(__name__)
app.config.from_object('config')

from momentjs import momentjs
app.jinja_env.globals['momentjs'] = momentjs

from version import version
app.jinja_env.globals['VERSION'] = version



db = SQLAlchemy(app)

from app import views, models


