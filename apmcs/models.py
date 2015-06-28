from apmcs import db
from apmcs import app

class Farmer(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(120))
    village = db.Column(db.String(80))
    area = db.Column(db.Integer)
    phone = db.Column(db.String(10))
    transactions = db.relationship('Transaction', backref='farmer', lazy='dynamic')

    def __init__(self, name, village, area, phone):
        self.name = name
        self.village = village
        self.area = int(area)
        self.phone = phone

    def __repr__(self):
        return '<Farmer %d %s %s %d %s>'%(self.id,self.name,self.village,\
                                          self.area, self.phone)

class Trader(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(120))
    village = db.Column(db.String(80))
    phone = db.Column(db.String(10))
    transactions = db.relationship('Transaction', backref='trader', lazy='dynamic')
    
    def __init__(self, name, village, phone):
        self.name = name
        self.village = village
        self.phone = phone

    def __repr__(self):
        return '<Trader %d %s %s %s>'%(self.id,self.name,self.village,\
                                          self.phone)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    date = db.Column(db.DateTime)
    trader_id = db.Column(db.Integer, db.ForeignKey('trader.id'))
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.id'))
    crop = db.Column(db.String(30))
    weight = db.Column(db.Numeric)
    price = db.Column(db.Numeric)
    commission = db.Column(db.Numeric)
    labour = db.Column(db.Numeric)
    total = db.Column(db.Numeric)

    def __init__(self, date, trader_id, farmer_id, crop, weight,\
                 price, commission, labour, total):
        self.date = date
        self.trader_id = trader_id 
        self.farmer_id = farmer_id
        self.crop = crop
        self.weight = weight
        self.price = price
        self.commission = commission
        self.labour = labour
        self.total = total

    def __repr__(self):
        return '<Transaction %s %s %s %s %d %d %d>'%(self.date ,self.trader ,self.farmer,\
                                          self.crop, self.weight, self.price, self.total)
