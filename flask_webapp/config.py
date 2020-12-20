from env_vars import db_key

class Config:
	SECRET_KEY = db_key
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	# to silence SQL warning
	SQLALCHEMY_TRACK_MODIFICATIONS = False