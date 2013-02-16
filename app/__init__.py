from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from dateutil import parser

import time
from flask import g

app = Flask(__name__)
app.config.from_object('config')

from momentjs import momentjs
app.jinja_env.globals['momentjs'] = momentjs

from version import version
app.jinja_env.globals['VERSION'] = version

# need to pull in the date from the file and put it in a global variable
f = open('app/version-date.txt', 'r')
data = f.read()
version_date = parser.parse(data)
f.close()
app.jinja_env.globals['VERSION_DATE'] = version_date

# pull in git describe
f = open('app/version-describe.txt', 'r')
data = f.read()
version_describe = data
f.close()
app.jinja_env.globals['VERSION_DESCRIBE'] = version_describe


print data
print version_date


db = SQLAlchemy(app)

from app import views, models


