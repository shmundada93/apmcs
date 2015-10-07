from apmcs import db
from apmcs import app
import datetime
from sqlalchemy import select, func, DateTime
from sqlalchemy.sql import case
from sqlalchemy.orm import column_property
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.expression import join


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow() \
                                          + datetime.timedelta(hours=5.5))
    content = db.Column(db.UnicodeText())
    group = db.Column(db.String(80))
    info = db.Column(db.String(250))

    def __init__(self, content="", group="", info=""):
        self.content = content
        self.group = group
        self.info = info


class Trader(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120))
    village = db.Column(db.String(80))
    phone = db.Column(db.String(10))

    def __init__(self, name="", village="", phone=""):
        self.name = name
        self.village = village
        self.phone = phone

    def __repr__(self):
        return '%s' % (self.name)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'))
    commodity = db.relationship('Commodity', backref='transactions')
    trader_id = db.Column(db.Integer, db.ForeignKey('trader.id'))
    trader = db.relationship('Trader', backref='transactions')
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.id', ondelete='CASCADE'))
    farmer = db.relationship('Farmer', backref='transactions')
    weight = db.Column(db.Numeric)
    price = db.Column(db.Numeric)
    commission = db.Column(db.Numeric)
    labour = db.Column(db.Numeric)
    total = db.Column(db.Numeric)

    def __init__(self, date, trader_id, farmer_id, commodity_id, weight, \
                 price, commission, labour, total):
        self.date = date
        self.commodity_id = commodity_id
        self.trader_id = trader_id
        self.farmer_id = farmer_id
        self.weight = weight
        self.price = price
        self.commission = commission
        self.labour = labour
        self.total = total

    def __repr__(self):
        return '%d %s\n%s Rs.%d' % (self.id, self.date, self.commodity, self.total)


class Commodity(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120))
    comm_percent = db.Column(db.Numeric)
    labour_perQtl = db.Column(db.Numeric)
    base_price = db.Column(db.Numeric)
    imageurl = db.Column(db.String)

    def __init__(self, name="", comm_percent=0, labour_perQtl=0, base_price=0,\
                 imageurl=""):
        self.name = name
        self.comm_percent = comm_percent
        self.labour_perQtl = labour_perQtl
        self.base_price = base_price
        self.imageurl = imageurl

    def __repr__(self):
        return '%s' % self.name


class Farmer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120))
    birth_date = db.Column(db.DateTime)
    village = db.Column(db.String(80))
    area = db.Column(db.Integer)
    phone = db.Column(db.String(10))

    @hybrid_property
    def amount(self):
        if self.transactions:
            return sum([transaction.total for transaction in self.transactions])
        else:
            return 0

    @amount.expression
    def amount(cls):
        return select([func.sum(Transaction.total)]). \
            where(Transaction.farmer_id == cls.id).label("amount")

    def __init__(self, name="", village="", area=None, phone="", birth_date=None):
        self.name = name
        self.village = village
        self.area = int(area)
        self.phone = phone
        self.birth_date = birth_date

    def __repr__(self):
        return "%s\n%s" % (self.name, self.phone)
