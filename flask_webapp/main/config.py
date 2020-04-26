import os

class Config:
	# adding secret key for security
	# grabbed from "secerets" python module
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	# to silence SQL warning
	SQLALCHEMY_TRACK_MODIFICATIONS = False
