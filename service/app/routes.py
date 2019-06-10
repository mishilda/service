#-*- coding: UTF-8 -*-
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, ClientForm, OrderForm, ReportForm, OrderFindForm, YearReportForm
from app import controllers
from app.models import User, Client, Order
from datetime import datetime, date

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		if controllers.authorization(form):
			return redirect(request.args.get('next') or url_for('index'))
		else:   	
			flash('Неверный логин или пароль')
			return redirect(url_for('login'))
	return render_template('login.html', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/clients')
def clients():
	clients = controllers.find_all_clients()
	return render_template('clients.html', clients=clients)

@app.route('/client/<id>')
def client(id):
	client = controllers.find_client(id)
	return render_template('client.html', client=client)

@app.route('/orders', methods=['GET', 'POST'])
def orders():
	form = OrderFindForm()
	if form.validate_on_submit():
		orders = controllers.find_orders_by_period(form.year.data, form.month.data)
		return render_template('orders.html', form=form, orders=orders, month=controllers.find_month(form.month.data), year=form.year.data)
	else: 
		orders = controllers.find_all_orders()
		return render_template('orders.html', form=form, orders=orders)
	
@app.route('/order/<id>')
def order(id):
	order = controllers.find_order(id)
	client = controllers.find_client(order.client_id)
	return render_template('order.html', order=order, client=client)

@app.route('/report')
def report():
	years, sum_for_year, global_sum = controllers.count_global()
	year_dict=enumerate(years)
	return render_template('report.html', years=year_dict, sum_for_year=sum_for_year, global_sum=global_sum)
	
@app.route('/report_for_this_year')
def report_for_this_year():
	year = date.today().year
	months, sum_for_month, global_sum = controllers.count_year(year)
	return render_template('report_for_this_year.html', year=year, months=months, sum_for_month=sum_for_month, global_sum=global_sum)

@app.route('/report_for_this_month')
def report_for_this_month():
	year = date.today().year
	month = date.today().month
	orders, global_sum = controllers.count_month(year, month)
	print(year, month)
	return render_template('report_for_this_month.html', year=year, month=controllers.find_month(month), orders=orders, global_sum=global_sum)

@app.route('/report_for_year', methods=['GET', 'POST'])
def report_for_year():
	form = YearReportForm()
	if form.validate_on_submit():
		months, sum_for_month, global_sum = controllers.count_year(form.year.data)
		return render_template('report_for_year.html', year=form.year.data, months=months, sum_for_month=sum_for_month, global_sum=global_sum, form=form)
	else:
		return render_template('report_for_year.html', year=0, months=[], sum_for_month=[], global_sum=0, form=form)

@app.route('/report_for_month', methods=['GET', 'POST'])
def report_for_month():
	form = ReportForm()
	if form.validate_on_submit():
		orders, global_sum = controllers.count_month(form.year.data, form.month.data)
		return render_template('report_for_month.html', year=form.year.data, month=controllers.find_month(form.month.data), orders=orders, global_sum=global_sum, form=form)
	else:
		return render_template('report_for_month.html', year=0, month=0, orders=[], global_sum=0, form=form)

@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
	form = ClientForm()
	if form.validate_on_submit():
		client = controllers.add_client(form)
		return redirect(url_for('client', id=client.id))
	return render_template('new_client.html', form=form)

@app.route('/edit_client/<id>', methods=['GET', 'POST'])
def edit_client(id):
	form = ClientForm()
	if form.validate_on_submit():
		print('cont')
		client = controllers.edit_client(id, form)
		print('/cont')
		return redirect(url_for('client', id=client.id))
	elif request.method == 'GET':
		client = controllers.find_client(id)
		controllers.fill_client_form(client, form)
	return render_template('edit_client.html', client=client, form=form)

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
	form = OrderForm()
	clients = controllers.find_all_clients()
	form.client.choices = [(client.id, client.name) for client in clients]
	if form.validate_on_submit():
		order = controllers.add_order(form)
		return redirect(url_for('order', id=order.id))
	else:
		return render_template('new_order.html', form=form)
	
@app.route('/edit_order/<id>', methods=['GET', 'POST'])
def edit_order(id):
	form = OrderForm()
	clients = controllers.find_all_clients()
	form.client.choices = [(client.id, client.name) for client in clients]
	if form.validate_on_submit():	
		order = controllers.edit_order(id, form)
		return redirect(url_for('order', id=order.id))
	elif request.method == 'GET':
		order = controllers.find_order(id)
		controllers.fill_order_form(order, form)
	return render_template('edit_order.html', order=order, form=form)
	
	
	
	