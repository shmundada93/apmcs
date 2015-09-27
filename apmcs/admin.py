from flask import Flask, redirect, request
from flask_admin import Admin, BaseView, expose
from flask_admin.model import BaseModelView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.filters import FloatGreaterFilter, FloatSmallerFilter
from sqlalchemy.sql.expression import func
from apmcs import admin, db, app
from apmcs.models import Farmer, Trader, Transaction, Commodity, Message, Email
from util import send_sms

Groups = {"silver": [0, 200000], "gold": [200001, 500000], "platinum": [500001, 1000000000]}


def groupFarmers(farmers, group=["silver", "gold", "platinum"]):
    groupNo = {"silver": 0, "gold": 0, "platinum": 0}
    phoneNos = []
    for farmer in farmers:
        amount = 0
        if farmer.transactions:
            amount = sum([transaction.total for transaction in farmer.transactions])
        for g in group:
            if amount >= Groups[g][0] and amount < Groups[g][1]:
                groupNo[g] += 1
                phoneNos.append(farmer.phone)
    return (groupNo, phoneNos)


class NewSMS(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        if request.method == 'POST':
            sms = request.form['sms']
            group = request.form.getlist('group')
            msg = Message(content=sms, group=" ".join(group), info="Sending SMS")
            db.session.add(msg)
            db.session.commit()
            farmers = Farmer.query.all()
            groupNo, phone_no = groupFarmers(farmers, group)
            send_sms(text=sms, phone_no=phone_no, msg_id=msg.id)
            return redirect('/admin/message')

        farmers = Farmer.query.all()
        groupNo, phoneNos = groupFarmers(farmers)
        return self.render('admin/message.html', groupNo=groupNo)


class EmailAdmin(ModelView):
    column_list = ['id', 'name', 'email']
    column_display_pk = True

    def __init__(self, session, name, category):
        super(EmailAdmin, self).__init__(Email, session, name, category)


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
        return redirect('/contact')


class MessageAdmin(ModelView):
    can_create = False
    can_delete = False
    column_list = ['id', 'date', 'content', 'group', 'info']
    column_display_pk = True
    column_formatters = dict(date=lambda v, c, m, p: m.date.strftime("%d %B %Y"))
    column_sortable_list = ['date']
    column_filters = ['date', 'group', 'info']
    column_default_sort = ('id')
    column_editable_list = ['content', ]

    def __init__(self, session, name, category):
        super(MessageAdmin, self).__init__(Message, session, name, category)


class FarmerAdmin(ModelView):
    column_list = ['id', 'name', 'village', 'phone', 'area', 'amount']
    column_display_pk = True
    column_descriptions = dict(amount="All Transactions Total (Rs.)")
    column_searchable_list = ['name', 'village', 'phone']
    column_editable_list = ['phone', ]
    column_sortable_list = ['id', 'name', 'village', 'area', 'amount']
    column_filters = ['village', 'area']  # ,FloatGreaterFilter(Farmer.amount,'Amount'),\
    # FloatSmallerFilter(Farmer.amount,'Amount')]
    inline_models = (Transaction,)

    def __init__(self, session):
        super(FarmerAdmin, self).__init__(Farmer, session)


class TransactionAdmin(ModelView):
    column_list = ('id', 'date', 'commodity', 'trader', 'farmer', 'weight', 'price', 'total')
    column_display_pk = True
    column_formatters = dict(date=lambda v, c, m, p: m.date.strftime("%d %B %Y"))
    column_sortable_list = ('date', ('commodity', 'commodity.name'), ('trader', 'trader.name'), \
                            ('farmer', 'farmer.name'), 'weight', 'price', 'total')
    column_searchable_list = ('commodity.name', 'trader.name', 'farmer.name')
    column_default_sort = ('date', True)
    column_filters = (
    'date', 'commodity.name', 'trader.name', 'farmer.name', 'farmer.village', 'weight', 'price', 'total')

    def __init__(self, session):
        super(TransactionAdmin, self).__init__(Transaction, session)


admin.add_view(NewSMS(name='New SMS', category="Messages"))
admin.add_view(MessageAdmin(db.session, name="All SMS", category="Messages"))
admin.add_view(FarmerAdmin(db.session))
admin.add_view(TransactionAdmin(db.session))
admin.add_view(ModelView(Trader, db.session))
admin.add_view(ModelView(Commodity, db.session))
admin.add_view(EmailAdmin(db.session, name="Email", category="Settings"))
admin.add_view(FrontPage(name='Home page', category='Other Pages'))
admin.add_view(TransactionLogger(name='Transaction Logger', category='Other Pages'))
admin.add_view(ContactPage(name='Contact Us', category='Other Pages'))
