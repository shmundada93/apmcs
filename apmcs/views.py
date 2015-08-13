# -*- coding: utf-8 -*-

from apmcs import app, db
from flask import Flask, render_template, url_for, request, redirect, session, g
from .models import Farmer, Trader, Transaction, Commodity
from config import SENTLY_AUTH
import datetime
import thread
from urllib2 import Request, urlopen
from urllib import urlencode
import json

#text = "Welcome to NN APMC. You are subscribed to pricing and your crop related information via SMS."
text = u'ना. ना. मुंदडा कृषि उत्पन्न बॅज़ार'
sender_id = "NNMAPM"
month_map = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,\
             'July':7,'August':8,'September':9,'October':10,'November':11,\
             'December':12}
    
def send_sms(sender_id, text, phone):
    values = {
        "from":sender_id,
        "to":"+91" + phone,
        "text":text}

    headers = {
    'Content-Type':'application/json',
    'Accept':'application/json',
    'Authorization':'Bearer adkk2y5yai7m5u039aketayl0kokdvhk',
    'Accept-Encoding':'gzip'}

    request = Request('https://apiserver.sent.ly/api/outboundmessage'\
                      ,data=json.dumps(values),headers=headers)
    response_body = urlopen(request).read()
    print response_body
    return None
    
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/u/search', methods = ['GET','POST'])
def farmer_search():
    if request.method == 'POST':
        try:
            farmer_id = int(request.form['name'])
            return redirect('/u/transaction/%d'%farmer_id)
        except:
            return render_template('registration.html', name = request.form['name'])
    farmers = Farmer.query.all()
    return render_template('search.html', farmers = farmers)

@app.route('/u/register', methods = ['GET','POST'])
def farmer_registration(name=""):
    if request.method == 'POST':
        name = request.form['name']
        village = request.form['village']
        area = int(request.form['area'])
        phone = request.form['phone']
        farmer = Farmer(name=name, village=village, area=area, phone=phone)
        db.session.add(farmer)
        db.session.commit()
        try:
            thread.start_new_thread(send_sms,(sender_id, text, phone,)) 
        except:
            pass    
        return redirect('/u/transaction/%d'%farmer.id)

    return render_template('registration.html', name = name)
    

@app.route('/u/transaction/<int:farmer_id>', methods = ['GET','POST'])
def farmer_transaction(farmer_id = None):
    if request.method == 'POST':
        date = request.form['date']
        (day,month,year) = date.split()
        date = datetime.datetime(int(year),month_map[month],int(day))
        commodity_id = request.form['commodity']
        trader_id = request.form['trader']
        weight = round(float(request.form['weight']),2)
        price = round(float(request.form['price']),2)
        commission = round(weight * price * 0.01,2)
        labour = round(weight * 7, 2)
        total = weight * price - commission - labour
        transaction = Transaction(date, trader_id, farmer_id, commodity_id, weight,\
                                  price, commission, labour, total)
        db.session.add(transaction)
        db.session.commit()
        
        return redirect('/u/invoice/%d'%transaction.id)
    
    farmer = Farmer.query.get(farmer_id)
    traders = Trader.query.all()
    commodities = Commodity.query.all()
    return render_template('transaction.html', farmer = farmer, \
                           commodities = commodities, traders = traders)

@app.route('/u/invoice/<int:transaction_id>')
def farmer_invoice(transaction_id = None):
    transaction = Transaction.query.get(transaction_id)
    date = transaction.date.strftime("%d - %B %Y")
    subtotal = round(transaction.weight*transaction.price,2)
    return render_template('invoice.html', date = date,\
                           transaction = transaction, subtotal = subtotal)
