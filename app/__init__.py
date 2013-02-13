from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


import time
from flask import g

app = Flask(__name__)
app.config.from_object('config')

from momentjs import momentjs
app.jinja_env.globals['momentjs'] = momentjs

db = SQLAlchemy(app)

from app import views, models

@app.before_request
def before_request():
  g.start = time.time()
