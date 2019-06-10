from app import db, login
from flask_login import UserMixin

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20))
	password = db.Column(db.String(50))
	email = db.Column(db.String(100))
	name = db.Column(db.String(100))

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class Client(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	car_num = db.Column(db.String(10))
	car_model = db.Column(db.String(50))
	car_colour = db.Column(db.String(50))
	passport = db.Column(db.String(15))
	phone = db.Column(db.String(11))

	def insert(self):
		db.session.add(self)
		db.session.commit()

	def update(self):
		db.session.add(self)
		db.session.commit()

class Order(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	client_id = db.Column(db.Integer)
	user_id = db.Column(db.Integer)
	date = db.Column(db.Date)
	cause = db.Column(db.String(500))
	guarantee = db.Column(db.Boolean)
	price = db.Column(db.Float)

	def select(date_from, date_to):
		return db.session.query(Order).filter(Order.date.between(date_from, date_to),).all()	
	def insert(self):
		db.session.add(self)
		db.session.commit()
	
	def update(self):
		db.session.commit()