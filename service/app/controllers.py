from app.models import User, Client, Order
from flask import redirect, url_for, request
from flask_login import login_user, current_user
from datetime import datetime, date
import calendar

def authorization(form):
	user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
	if user is not None:
		login_user(user, remember=form.remember_me.data)
		return True
	return False

def find_all_clients():
	return Client.query.all()

def find_client(id):
	return Client.query.get(int(id))

def find_all_orders():
	return Order.query.all()

def find_orders_by_period(year, month):
	date_from = date(year=year, month=month, day=1)
	date_to = date(year=year, month=month, day=calendar.monthrange(year, month)[1])
	orders = Order.select(date_from, date_to)
	if orders is None:
		return []
	else: return orders

def find_order(id):
	return Order.query.get(int(id))

def count_month(year, month):
	orders = find_orders_by_period(year, month)
	global_sum = 0
	for order in orders:
		global_sum +=  order.price
	return orders, global_sum

def count_year(year):
	sum_for_month_list = []
	months_name = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
	months = enumerate(months_name)
	global_sum = 0
	for i in range(1,13):
		sum_for_month = count_month(year, i)[1]
		sum_for_month_list.append(sum_for_month)
		global_sum += sum_for_month
	return months, sum_for_month_list, global_sum	
	
def count_global():
	sum_for_year_list = []
	global_sum = 0
	years = [i for i in range(2017, 2026)]
	for i in years:
		sum_for_year = count_year(i)[2]
		sum_for_year_list.append(sum_for_year)
		global_sum += sum_for_year
	return years, sum_for_year_list, global_sum
		                              
def add_client(form):
	client = Client(name=form.name.data, car_num=form.car_num.data, car_model=form.car_model.data, car_colour=form.car_colour.data, passport=form.passport.data, phone=form.phone.data)
	client.insert()
	return client

def edit_client(id, form):
	client = Client.query.filter_by(id=id).first()
	client.name = form.name.data
	client.car_num=form.car_num.data
	client.car_model=form.car_model.data
	client.car_colour=form.car_colour.data
	client.passport = form.passport.data
	client.phone = form.phone.data 
	client.update()
	return client

def fill_client_form(client, form):
	form.name.data = client.name
	form.passport.data = client.passport
	form.phone.data = client.phone
	form.car_num.data = client.car_num
	form.car_model.data = client.car_model
	form.car_colour.data = client.car_colour

def add_order(form):
	order = Order(client_id=form.client.data, user_id=current_user.id, date=date.today(), cause=form.cause.data, guarantee=form.guarantee.data, price=form.price.data)
	order.insert()
	return order

def edit_order(id, form):
	order = Order.query.filter_by(id=id).first()
	order.client_id = form.client.data
	order.cause = form.cause.data
	order.guarantee = form.guarantee.data
	order.price = form.price.data
	order.update()
	return order

def fill_order_form(order, form):
	form.client.data = order.client_id
	form.cause.data = order.cause
	form.guarantee.data = order.guarantee
	form.price.data = order.price	
			
def find_month(month):
	months_name = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
	return months_name[month-1]
	 