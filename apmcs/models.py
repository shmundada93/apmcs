from apmcs import db
from apmcs import app

class Farmer(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(120))
    village = db.Column(db.String(80))
    area = db.Column(db.Integer)
    phone = db.Column(db.String(10))
    transactions = db.relationship('Transaction', backref='farmer', lazy='dynamic')

    def __init__(self, name="", village="", area=None, phone=""):
        self.name = name
        self.village = village
        self.area = int(area)
        self.phone = phone

    def __repr__(self):
        return '%d %s\n%s'%(self.id,self.name,self.phone)

class Trader(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(120))
    village = db.Column(db.String(80))
    phone = db.Column(db.String(10))
    transactions = db.relationship('Transaction', backref='trader', lazy='dynamic')
    
    def __init__(self, name="", village="", phone=""):
        self.name = name
        self.village = village
        self.phone = phone

    def __repr__(self):
        return '%s\n%s\n%s'%(self.name,self.village,self.phone)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    date = db.Column(db.DateTime)
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'))
    trader_id = db.Column(db.Integer, db.ForeignKey('trader.id'))
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.id'))
    weight = db.Column(db.Numeric)
    price = db.Column(db.Numeric)
    commission = db.Column(db.Numeric)
    labour = db.Column(db.Numeric)
    total = db.Column(db.Numeric)

    def __init__(self, date, trader_id, farmer_id, commodity_id, weight,\
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
        return '%d %s\n%s Rs.%d'%(self.id,self.date, self.commodity,self.total)

class Commodity(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(120))
    comm_percent = db.Column(db.Numeric)
    labour_perQtl = db.Column(db.Numeric)
    transactions = db.relationship('Transaction', backref='commodity', lazy='dynamic')

    def __init__(self, name ="", comm_percent=0, labour_perQtl=0):
        self.name = name
        self.comm_percent = comm_percent
        self.labour_perQtl = labour_perQtl
    
    def __repr__(self):
        return '%s'%self.name
