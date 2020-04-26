from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_webapp import db, bcrypt
from flask_webapp.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_webapp.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_webapp.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm)
from flask_webapp.users.utils import save_picture

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	# checks if form was validated on submit
	if form.validate_on_submit():
		# storing user details from forms.py
		# hashing the pw
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pw)

		# add the created user to the db
		db.session.add(user)
		db.session.commit()
		flash('Account created successfully.', 'success')
		return redirect(url_for('users.login'))

		# give message / alert
		flash(f"Account created for {form.username.data}.",'success')
		return redirect(url_for('main.home'))
	return render_template('register.html', 
		title='Register', form = form)


@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():  
		# check what username (email) was entered during the singin
		user = User.query.filter_by(email=form.email.data).first()

		# if it exists
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			# use the login_user function and enter the user from above
			login_user(user, remember=form.remember.data)
			# redirecting the user to the page they were trying to access after signing in
			next_page = request.args.get('next')

			# if successful, redirect to home
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('Sign in failed. Please check details again.','danger')

	return render_template('login.html', 
		title='Sign In', form = form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		# profile picture upload
		if form.pic.data:
			pic_file = save_picture(form.pic.data)
			current_user.image_file = pic_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		# commit the changes in our DB
		db.session.commit()
		flash('Account updated.', 'success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email


	image_file = url_for('static',
		filename='profile_pics/'+current_user.image_file) 
	return render_template('account.html', title='Account',
		image_file = image_file, form=form)










