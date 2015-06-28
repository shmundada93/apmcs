from apmcs import app, db
from flask import Flask, render_template, url_for, request, redirect, session, g
from .models import Farmer, Trader, Transaction

@app.route('/u/search')
def farmer_search():
    return render_template('search.html')

@app.route('/u/register', methods = ['GET','POST'])
def farmer_registration():
    if request.method == 'POST':
        name = request.form['name']
        village = request.form['village']
        area = int(request.form['area'])
        phone = request.form['phone']
        farmer = Farmer(name=name, village=village, area=area, phone=phone)
        db.session.add(farmer)
        db.session.commit()
        return redirect('/u/transaction/%d'%farmer.id)
    return render_template('registration.html')
    

@app.route('/u/transaction/<int:farmer_id>', methods = ['GET','POST'])
def farmer_transaction(farmer_id = None):
    if request.method == 'POST':
        pass
    farmer = Farmer.query.get(farmer_id)
    return render_template('transaction.html', farmer = farmer)

@app.route('/u/invoice')
def farmer_invoice():
    return render_template('invoice.html')
