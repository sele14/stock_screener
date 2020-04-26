from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_webapp.models import User




class RegistrationForm(FlaskForm):
	# adding some requirements for the usernames
	# using validators
	# DataRequired means they cant input empty username field
	username = StringField('Username',
		validators=[DataRequired(), Length(min=2, max=20)]
		)
	email = StringField('Email',
		validators=[DataRequired(), Email()])
	password = PasswordField('Password',
		validators=[DataRequired()])

	confirm_pass = PasswordField('Confirm Password',
		validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Sign Up')

	# creating a custom validations for duplicate user registrations (e.g. user/email exists)
	def validate_username(self, username):
		# grab username entered in our registration form
		user = User.query.filter_by(username=username.data).first()

		# if user exists, send a validation error
		if user:
			raise ValidationError('Username already exists. Please choose a different username.')
	
	def validate_email(self, email):
		# grab email entered in our registration form
		user = User.query.filter_by(email=email.data).first()

		# if email exists, send a validation error
		if user:
			raise ValidationError('Email already exists. Please choose a different email.')


class LoginForm(FlaskForm):
	email = StringField('Email',
		validators=[DataRequired(), Email()])
	password = PasswordField('Password',
		validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


# allow user to update their credentials
class UpdateAccountForm(FlaskForm):
	username = StringField('Username',
		validators=[DataRequired(), Length(min=2, max=20)]
		)
	email = StringField('Email',
		validators=[DataRequired(), Email()])

	pic = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

	# these checks will be different than the above 
	# bc the user should still be able to enter their existing username
	# e.g. keeping their details as-is
	def validate_username(self, username):
		if username.data != current_user.username:
			# grab username entered in our registration form
			user = User.query.filter_by(username=username.data).first()

			# if user exists, send a validation error
			if user:
				raise ValidationError('Username already exists. Please choose a different username.')
	
	def validate_email(self, email):
		if email.data != current_user.email:
			# grab email entered in our registration form
			user = User.query.filter_by(email=email.data).first()

			# if email exists, send a validation error
			if user:
				raise ValidationError('Email already exists. Please choose a different email.')



