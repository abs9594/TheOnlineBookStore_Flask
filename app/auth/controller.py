from flask import Blueprint,request,jsonify,render_template,flash,redirect,url_for
from app.auth.forms import (RegistrationForm,LoginForm,UpdatePasswordForm,
	                        RequestResetForm,ResetPasswordForm)
from app.auth.models import User
from flask_login import login_user,logout_user,login_required,current_user
from flask_mail import Message
from app import mail

authentication = Blueprint("authentication",__name__)

@authentication.route("/register",methods=["GET","POST"])
def register_user():
	if current_user.is_authenticated:
		flash("You are already LoggedIn")
		return redirect(url_for('home_app.home'))
	form = RegistrationForm()

	if form.validate_on_submit():
		User.create_user(
		user=form.username.data,
		email=form.email_id.data,
		password=form.password.data,
		)
		flash("Registration Successfull","sucess")
		return redirect(url_for("authentication.do_the_login"))

	return render_template("authentication/registration.html",
	form=form)

@authentication.route("/login",methods=["GET","POST"])
def do_the_login():
	if current_user.is_authenticated:
		flash("You are already LoggedIn")
		return redirect(url_for('catalogue.home'))
	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(user_email=form.email.data).first()
		if not user:
			flash("User doesn't exist","error")
			return redirect(url_for('authentication.do_the_login'))
		
		elif not user.check_password(form.password.data):
			flash("Invalid password","error")
			return redirect(url_for('authentication.do_the_login'))
		login_user(user,form.stay_loggedin.data)
		return redirect(url_for('catalogue.home'))

	return render_template("authentication/login.html",form=form)

@authentication.route('/logout')
@login_required
def log_out_user():
	logout_user()
	return redirect(url_for('authentication.do_the_login'))

@authentication.app_errorhandler(404)
def page_not_found(error):
	return render_template('authentication/page_not_found.html'),404


@authentication.route("/oauth2callback",methods=["GET"])
def do_the_google_login():
	if current_user.is_authenticated:
		flash("You are already LoggedIn")
		return redirect(url_for('catalogue.home'))

	form = RegistrationForm()
	flash("This Feature of Google Login is coming soon, please consider registering with us!")
	return render_template("authentication/registration.html",
	form=form)

@authentication.route("/updatepassword",methods=["GET","POST"])
@login_required
def update_password():
	form = UpdatePasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(user_email=form.email.data).first()
		if not user:
			flash("User does not exists","error")
			return redirect(url_for("authenticatoion.update_password"))
		
		elif not user.check_password(form.current_password.data):
			# print(form.current_password.data)
			flash("Invalid password","error")
			return redirect(url_for('authentication.update_password'))
		user.update_password(form.new_password.data)
		flash("Password Updated Sucessfully","green")
		return redirect(url_for('catalogue.home'))
		
	form.email.data = current_user.user_email	
	return render_template("authentication/update_password.html",form=form)

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message("Password Reset Request",sender='noreply@thenewonlinebookstore.com',
		  recipients=[user.user_email])
	msg.body = f''' To reset your password, visit the following link:
	{url_for('authentication.reset_password_set',token=token,_external=True)}

	If you did not make this request then please ignore this mail

	'''

	mail.send(msg)

@authentication.route("/resetpassword",methods=["GET","POST"])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('catalogue.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(user_email=form.email.data).first()
		if not user:
			flash("User does not exists","error")
			return redirect(url_for("authenticatoion.reset_password_request"))
		send_reset_email(user)
		flash("An email has been sent with instruction to reset your password","sucess")
		return redirect(url_for('authentication.do_the_login'))
		
	return render_template("authentication/reset_password_request.html",form=form)

@authentication.route("/resetpassword/<token>",methods=["GET","POST"])
def reset_password_set(token):
	if current_user.is_authenticated:
		return redirect(url_for('catalogue.home'))
	user = User.verify_reset_token(token)
	if not(user):
		flash("Token is invalid or expired","error")
		return redirect(url_for("authentication.reset_password_request"))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(user_email=form.email.data).first()
		if not user:
			flash("User does not exists","error")
			return redirect(url_for("authenticatoion.update_password"))
		
		user.update_password(form.new_password.data)
		
		flash("Password Updated Sucessfully","green")
		return redirect(url_for('catalogue.home'))
	form.email.data = user.user_email
	return render_template("authentication/update_forgot_password.html",form=form)