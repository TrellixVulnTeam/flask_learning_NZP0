from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_login import current_user
from flask import flash


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField(
		'Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
	oldpassword=PasswordField('Old Password')
	password = PasswordField('New Password', )
	password2 = PasswordField(
		'Repeat Password', validators=[EqualTo('password')])
	submit = SubmitField('Submit')

	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if username.data == current_user.username:
			return
		if user is not None:
			raise ValidationError('Please use a different username.')
	def validate_oldpassword(self,oldpassword):
		flash("modifying for user: {}".format(current_user.username))
		if oldpassword.data and not current_user.check_password(password=oldpassword.data):
			raise ValidationError('Old Password not correct')

	def validate_password(self,password):
		if self.oldpassword.data and not password.data:
			raise ValidationError('For changing password, please file new password field')