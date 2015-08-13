from flask import Flask, redirect
from flask_admin import Admin, BaseView, expose
from flask_admin.model import BaseModelView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.filters import FloatGreaterFilter,FloatSmallerFilter
from sqlalchemy.sql.expression import func
from apmcs import admin, db, app
from apmcs.models import Farmer, Trader, Transaction, Commodity

class FrontPage(BaseView):
    @expose('/')
    def index(self):
        return redirect('/')

class TransactionLogger(BaseView):
    @expose('/')
    def index(self):
        return redirect('/u/search')

class ContactPage(BaseView):
    @expose('/')
    def index(self):
        return redirect('/contacts')

class FarmerAdmin(ModelView):

    column_list = ['id','name','village','phone','area','amount']

    column_display_pk = True
    
    column_descriptions = dict(amount = "All Transactions Total (Rs.)")

    column_searchable_list = ['name','village','phone']
    
    column_editable_list = ['phone',]

    column_sortable_list = ['id','name','village','area','amount']

    column_filters = ['village','area']#,FloatGreaterFilter(Farmer.amount,'Amount'),\
                      #FloatSmallerFilter(Farmer.amount,'Amount')]
    
    inline_models = (Transaction,)

##    def get_query(self):
##        return self.session.query(
##            Farmer.id.label("id"),
##            Farmer.name.label("name"),
##            Farmer.village.label("village"),
##            Farmer.phone.label("phone"),
##            Farmer.area.label("area"),
##            func.sum(Transaction.total).label("amount")
##            ).join(Transaction).group_by(Farmer.id)

##    def scaffold_sortable_columns(self):
##        return {'id':'id','name':'name','village':'village',\
##                'area':'area','amount':'amount'}

##    def scaffold_list_columns(self):
##        return ['id','name','village','phone','area','amount']

##    def scaffold_filters(self,name):
##        filters = super(FarmerAdmin, self).scaffold_filters(name)
##        print filters
##        return filters

    def __init__(self, session):
        super(FarmerAdmin, self).__init__(Farmer, session)

class TransactionAdmin(ModelView):
    column_list = ('date' , 'commodity' , 'trader' , 'farmer' , 'weight' , 'price', 'total')

    column_display_pk = True
    
    column_formatters = dict(date=lambda v,c,m,p: m.date.strftime("%d %B %Y"))
    
    column_sortable_list = ('date', ('commodity', 'commodity.name'), ('trader', 'trader.name'),\
                            ('farmer', 'farmer.name'),'weight', 'price', 'total')

    column_searchable_list = ('commodity.name', 'trader.name', 'farmer.name')

    column_default_sort = ('date',True)

    column_filters = ('date', 'commodity.name', 'trader.name', 'farmer.name', 'farmer.village','weight', 'price', 'total')

    def __init__(self, session):
        super(TransactionAdmin, self).__init__(Transaction, session)
        

admin.add_view(ModelView(Commodity, db.session))
admin.add_view(TransactionAdmin(db.session))
admin.add_view(ModelView(Trader, db.session))
admin.add_view(FarmerAdmin(db.session))
admin.add_view(FrontPage(name='Front page', category='Other Pages'))
admin.add_view(TransactionLogger(name='Transaction Logger', category='Other Pages'))
admin.add_view(ContactPage(name='Contact Us', category='Other Pages'))


