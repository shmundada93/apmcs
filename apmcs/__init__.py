from flask import Flask
from flask_admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.basicauth import BasicAuth

app = Flask(__name__)
admin = Admin(app, template_mode='bootstrap3')

app.config.from_object('config')
app.config['BASIC_AUTH_FORCE'] = False

db = SQLAlchemy(app)

BasicAuth(app)

import apmcs.views, apmcs.models, apmcs.admin
