from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length

years = [(i, i) for i in range(2017, 2026)]
month = [(1, 'Январь'), (2, 'Февраль'), (3, 'Март'), (4, 'Апрель'), (5, 'Май'), (6, 'Июнь'), (7, 'Июль'), (8, 'Август'), (9, 'Сентябрь'), (10, 'Октябрь'), (11, 'Ноябрь'), (12, 'Декабрь')]


class LoginForm(FlaskForm):
	username = StringField('Логин', validators=[DataRequired()])
	password = PasswordField('Пароль', validators=[DataRequired()])
	remember_me = BooleanField('Запомнить меня')
	submit = SubmitField('Войти')

class ClientForm(FlaskForm):
	name = StringField('ФИО', validators=[DataRequired()])
	passport = StringField('Паспортные данные', validators=[DataRequired()])
	phone = StringField('Контактный телефон', validators=[DataRequired()])
	car_num = StringField('Номер автомобиля', validators=[DataRequired()])
	car_model = StringField('Марка автомобиля', validators=[DataRequired()])
	car_colour = StringField('Цвет автомобиля', validators=[DataRequired()])
	submit = SubmitField('Записать')
	
class OrderForm(FlaskForm):
	client = SelectField('Клиент', coerce=int)
	cause = TextAreaField('Цель обслуживания', validators=[DataRequired()])
	guarantee = BooleanField('Гарантийное обслуживание')
	price = StringField('Стоимость обслуживания', validators=[DataRequired()])
	submit = SubmitField('Оформить')

class ReportForm(FlaskForm):     
	year = SelectField('Год отчета', coerce=int, choices=years)
	month = SelectField('Месяц отчета', coerce=int, choices=month)
	submit = SubmitField('Найти')
	
class OrderFindForm(FlaskForm):
	year = SelectField('Выберите год', coerce=int, choices=years)
	month = SelectField('Выберите месяц', coerce=int, choices=month)
	submit = SubmitField('Найти')

class YearReportForm(FlaskForm):
	year = SelectField('Год отчета', coerce=int, choices=years)
	submit = SubmitField('Найти')