from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_webapp.config import Config

# This file initialises our app.

# creating a DB instance
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'




def create_app(config_class=Config):
	# set an instance of the flask app passing in "__name__"
	app = Flask(__name__)
	app.config.from_object(Config)
	
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)

	# importing blueprints and adding to app
	from flask_webapp.users.routes import users
	from flask_webapp.main.routes import main
	app.register_blueprint(users)
	app.register_blueprint(main)

	# with app.app_context():
	# 	# import dash app
	# 	from flask_webapp.dashapp.dash_app import Add_Dash
	# 	app = Add_Dash(app)
	from flask_webapp.dashapp.dash_app import Add_Dash
	app = Add_Dash(app)

	return app

