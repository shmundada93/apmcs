from flask import Flask
from flask_admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.basicauth import BasicAuth
from config import APPLICATION_ID, REST_API_KEY, MASTER_KEY
from parse_rest.connection import register


app = Flask(__name__)
admin = Admin(app, template_mode='bootstrap3')

app.config.from_object('config')
app.config['BASIC_AUTH_FORCE'] = False
register(APPLICATION_ID, REST_API_KEY)

db = SQLAlchemy(app)

BasicAuth(app)

import apmcs.views, apmcs.models, apmcs.admin
from flask.ext.assets import Bundle, Environment
bundles = {

    'home_js': Bundle(
        'js/jquery.min.js',
        'js/bootstrap.min.js',
        output='gen/home.js',
        filters='jsmin'),

    'home_css': Bundle(
        'css/bootstrap.min.css',
        'css/bootstrap-theme.min.css',
        output='gen/home.css',
        filters='cssmin'),
}

assets = Environment(app)

assets.register(bundles)
