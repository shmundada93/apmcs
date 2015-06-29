from flask import Flask
from flask_admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
admin = Admin(app)

app.config.from_object('config')

db = SQLAlchemy(app)


import apmcs.views, apmcs.models, apmcs.admin

