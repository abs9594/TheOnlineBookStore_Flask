from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,validators,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo,Email,ValidationError
from wtforms.fields.html5 import EmailField
from app.auth.models import User


def email_exists(form,field):
	email = User.query.filter_by(user_email=field.data).first()
	if email:
		raise ValidationError("Email Already Exists")


class RegistrationForm(FlaskForm):

	username = StringField("Username",validators=[DataRequired(),
		Length(min=4, max=8,message="Username should be minimum 4 and maximum 20 characters Long")])
	
	email_id = EmailField("Email",validators=[DataRequired(),Email(),email_exists])
	
	password = PasswordField("Password",validators=[DataRequired(),
		Length(min=4, max=20,message="Password should be minimum 8 and maximum 20 characters Long"),
		EqualTo('confirm_password',message="Your password and confirmation password do not match")])

	confirm_password = PasswordField('Confirm Password',
             validators=[DataRequired(),
             EqualTo('password',message="Your password and confirmation password do not match")])

	submit = SubmitField("Register")


class LoginForm(FlaskForm):

	email = StringField('Email',validators=[DataRequired(),Email()])
	
	password = PasswordField('Password',validators=[DataRequired()])
	
	stay_loggedin = BooleanField('stay logged-in')
	
	submit = SubmitField('LogIn')


class UpdatePasswordForm(FlaskForm):

	email = StringField('Email',validators=[DataRequired(),Email()])

	current_password = PasswordField('Current Password',validators=[DataRequired()])

	new_password = PasswordField('New Password',validators=[DataRequired(),
		Length(min=4, max=20,message="Password should be minimum 8 and maximum 20 characters Long"),
		EqualTo('new_password_confirm',message="Your password and confirmation password do not match")])

	new_password_confirm = PasswordField('Confirm New Password',validators=[DataRequired(),
		Length(min=4, max=20,message="Password should be minimum 8 and maximum 20 characters Long"),
		EqualTo('new_password',message="Your password and confirmation password do not match")])

	submit = SubmitField('Update')