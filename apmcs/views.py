# -*- coding: utf-8 -*-

from apmcs import app, db
from flask import Flask, render_template, url_for, request, redirect, session, g
from .models import Farmer, Trader, Transaction, Commodity, Message
from util import send_sms
import datetime
from parse_rest.datatypes import Object

#eMandi
class Item(Object):
    pass

def saveInParse(weight, commodity_id , farmer_id):
    item = Item()
    commodity = Commodity.query.get(commodity_id)
    farmer = Farmer.query.get(farmer_id)
    opentime = datetime.datetime.now() - datetime.timedelta(hours = 5, minutes=30)
    closetime = opentime + datetime.timedelta(hours = 2)
    item.name = commodity.name
    item.commodity_id = commodity.id
    item.description = """Base Price: Rs. %.2f\n

                          Quantity: %.2f Quintals\n
                          
                          Minimum Value: Rs. %.2f\n
                          
                          Parameters ....
                          """%(commodity.base_price, weight,\
                               weight*float(commodity.base_price))
    item.donorname = farmer.name
    item.farmer_id = farmer_id
    item.price = int(commodity.base_price)
    item.weight = weight
    item.priceIncrement = 1
    item.qty = 1
    item.currentPrice = []
    item.numberOfBids = 0
    item.allBidders = []
    item.currentWinners = []
    item.previousWinners = []
    item.opentime = opentime
    item.closetime = closetime
    item.type = "Boring"
    item.save()
    return True



month_map = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, \
             'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, \
             'December': 12}


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/u/search', methods=['GET', 'POST'])
def farmer_search():
    if request.method == 'POST':
        try:
            farmer_id = int(request.form['name'])
            return redirect('/u/transaction/%d' % farmer_id)
        except:
            farmers = Farmer.query.all()
            return render_template('registration.html', \
                                   name=request.form['name'], farmers=farmers)
    farmers = Farmer.query.all()
    return render_template('search.html', farmers=farmers)


@app.route('/u/register', methods=['GET', 'POST'])
def farmer_registration(name=""):
    if request.method == 'POST':
        birthdate = request.form['birthdate']
        if birthdate:
            (day, month) = birthdate.split()
            birthdate = datetime.datetime(2000, month_map[month], int(day))
        else:
            birthdate = None
        name = request.form['name']
        village = request.form['village']
        area = int(request.form['area'])
        phone = request.form['phone']
        farmer = Farmer(name=name, village=village, area=area, \
                        phone=phone, birth_date=birthdate)
        db.session.add(farmer)
        db.session.commit()
        msg = Message.query.get(1)
        send_sms(text=msg.content, phone_no=[phone])
        return redirect('/u/transaction/%d' % farmer.id)
    farmers = Farmer.query.all()
    return render_template('registration.html', name=name, farmers=farmers)


@app.route('/u/transaction/<int:farmer_id>', methods=['GET', 'POST'])
def farmer_transaction(farmer_id=None):
    if request.method == 'POST':
        date = request.form['date']
        (day, month, year) = date.split()
        date = datetime.datetime(int(year), month_map[month], int(day))
        commodity_id = request.form['commodity']
        trader_id = request.form['trader']
        weight = round(float(request.form['weight']), 2)
        price = round(float(request.form['price']), 2)
        commission = round(weight * price * 0.01, 2)
        labour = round(weight * 7, 2)
        total = weight * price - commission - labour
        transaction = Transaction(date, trader_id, farmer_id, commodity_id, weight, \
                                  price, commission, labour, total)
        db.session.add(transaction)
        db.session.commit()

        return redirect('/u/invoice/%d' % transaction.id)

    farmer = Farmer.query.get(farmer_id)
    traders = Trader.query.all()
    commodities = Commodity.query.all()
    return render_template('transaction.html', farmer=farmer, \
                           commodities=commodities, traders=traders)

@app.route('/u/farmer/<int:farmer_id>', methods=['POST'])
def update_farmer(farmer_id=None):
    if request.method == 'POST':
        farmer = Farmer.query.get(farmer_id)
        farmer.phone = request.form['phone']
        farmer.village = request.form['village']
        farmer.area = int(request.form['area'])
        birthdate = request.form['birthdate']
        if birthdate:
            (day, month) = birthdate.split()
            farmer.birth_date = datetime.datetime(2000, month_map[month], int(day))
        db.session.commit()
        return redirect('/u/transaction/%d' % farmer.id)
    
@app.route('/u/invoice/<int:transaction_id>')
def farmer_invoice(transaction_id=None):
    transaction = Transaction.query.get(transaction_id)
    date = transaction.date.strftime("%d - %B %Y")
    subtotal = round(transaction.weight * transaction.price, 2)
    return render_template('invoice.html', date=date, \
                           transaction=transaction, subtotal=subtotal)

@app.route('/mandi/post/<int:farmer_id>', methods=["GET","POST"])
def post_item(farmer_id=None):
    if request.method == "POST":
        weight = round(float(request.form['weight']), 2)
        commodity_id = request.form['commodity']
        saveInParse(weight, commodity_id, farmer_id)
        return "Done..."
    
    farmer = Farmer.query.get(farmer_id)
    traders = Trader.query.all()
    commodities = Commodity.query.all()
    return render_template('mtransaction.html', farmer=farmer, \
                           commodities=commodities, traders=traders)



@app.route('/mandi/search', methods=['GET', 'POST'])
def mfarmer_search():
    if request.method == 'POST':
        try:
            farmer_id = int(request.form['name'])
            return redirect('/mandi/post/%d' % farmer_id)
        except:
            farmers = Farmer.query.all()
            return render_template('mregistration.html', \
                                   name=request.form['name'], farmers=farmers)
    farmers = Farmer.query.all()
    return render_template('msearch.html', farmers=farmers)


@app.route('/mandi/register', methods=['GET', 'POST'])
def mfarmer_registration(name=""):
    if request.method == 'POST':
        birthdate = request.form['birthdate']
        if birthdate:
            (day, month) = birthdate.split()
            birthdate = datetime.datetime(2000, month_map[month], int(day))
        else:
            birthdate = None
        name = request.form['name']
        village = request.form['village']
        area = int(request.form['area'])
        phone = request.form['phone']
        farmer = Farmer(name=name, village=village, area=area, \
                        phone=phone, birth_date=birthdate)
        db.session.add(farmer)
        db.session.commit()
        msg = Message.query.get(1)
        send_sms(text=msg.content, phone_no=[phone])
        return redirect('/mandi/post/%d' % farmer.id)
    farmers = Farmer.query.all()
    return render_template('mregistration.html', name=name, farmers=farmers)

@app.route('/mandi/farmer/<int:farmer_id>', methods=['POST'])
def mupdate_farmer(farmer_id=None):
    if request.method == 'POST':
        farmer = Farmer.query.get(farmer_id)
        farmer.phone = request.form['phone']
        farmer.village = request.form['village']
        farmer.area = int(request.form['area'])
        birthdate = request.form['birthdate']
        if birthdate:
            (day, month) = birthdate.split()
            farmer.birth_date = datetime.datetime(2000, month_map[month], int(day))
        db.session.commit()
        return redirect('/mandi/post/%d' % farmer.id)
