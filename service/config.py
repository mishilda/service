import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):

	POSTGRES = {
		'user':'postgres',
		'pw':'123',
		'db':'Service',
		'host':'localhost',
		'port':'5432',
}

	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	SQLALCHEMY_DATABASE_URI = 'postgres://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s'%POSTGRES
	SQLALCHEMY_TRACK_MODIFICATIONS = False