from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from dateutil import parser

import os

import time
from flask import g
import string

app = Flask(__name__)
app.config.from_object('config')

from momentjs import momentjs
app.jinja_env.globals['momentjs'] = momentjs

from version import version
app.jinja_env.globals['VERSION'] = version

BASE_PATH = os.path.dirname(__file__)


# need to pull in the date from the file and put it in a global variable
f = open(BASE_PATH + '/version-date.txt', 'r')
data = f.read()
version_date = parser.parse(data)
f.close()
app.jinja_env.globals['VERSION_DATE'] = version_date

# pull in git describe
f = open(BASE_PATH + '/version-describe.txt', 'r')
data = f.read()
version_describe = string.replace(string.replace(data, '\n', ''), '\r', '')
f.close()
app.jinja_env.globals['VERSION_DESCRIBE'] = version_describe



db = SQLAlchemy(app)

from app import views, models


