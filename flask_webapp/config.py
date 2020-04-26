import os

class Config:
	# adding secret key for security
	# grabbed from "secerets" python module
	# SECRET_KEY = os.environ.get('SECRET_KEY')
	SECRET_KEY = 'b000ebc7b36952cf35e2'
	# SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

	# to silence SQL warning
	SQLALCHEMY_TRACK_MODIFICATIONS = False
