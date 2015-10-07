from flask.ext.assets import Bundle, Environment
from .. import app

bundles = {

    'home_js': Bundle(
        'js/lib/jquery.min.js',
        'js/bootstrap.min.js',
        output='gen/home.js',
        filters='jsmin'),

    'home_css': Bundle(
        'css/bootstrap.min.css',
        'css/bootstrap-theme.min.css',
        output='gen/home.css
        filters='cssmin'),
}

assets = Environment(app)

assets.register(bundles)
