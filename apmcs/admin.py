from flask import Flask
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from apmcs import admin, db, app
from apmcs.models import Farmer, Trader, Transaction, Commodity

class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')
    
admin.add_view(ModelView(Commodity, db.session))
admin.add_view(ModelView(Transaction, db.session))
admin.add_view(ModelView(Trader, db.session))
admin.add_view(ModelView(Farmer, db.session))

