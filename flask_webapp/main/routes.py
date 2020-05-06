from flask import render_template, request, Blueprint
from flask_webapp.models import Post
from flask_webapp.dashapp import dash_app

main = Blueprint('main', __name__)


# dummy data
posts = [
	# {	
	# 'author' : 'Eirik Selander',
	# 'title' : 'Blog Post 1',
	# 'content' : 'First post content',
	# 'date_posted' : 'April 20, 2018'
	# }
]


# route decorator (a way to add functionality to the function)
# devides how/where to access the specific page
@main.route('/') # the default page
@main.route('/home')
def home():
	# the content of the route is in a render_template html file which we create
	return render_template('home.html', posts=posts)

@main.route('/screener')
def screener():
	return render_template('screener.html', dash_url=dash_app.url_base, title='Stock Screener')

@main.route('/factor_invest')
def factor_invest():
	return render_template('factor_invest.html', title='Factor Investing Wiki')

@main.route('/machine_learning_wiki')
def machine_learning_wiki():
	return render_template('machine_learning_wiki.html', title='Machine Learning Wiki')
 
@main.route('/backtester')
def backtester():
	return render_template('backtester.html', title='Backtesting')
 


