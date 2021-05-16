from flask import Blueprint,request,jsonify,render_template,flash,redirect,url_for
from app.auth.forms import RegistrationForm,LoginForm,UpdatePasswordForm
from app.auth.models import User
from flask_login import login_user,logout_user,login_required,current_user

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
		flash("Registration Successfull")
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
			flash("User doesn't exist")
			return redirect(url_for('authentication.do_the_login'))
		
		elif not user.check_password(form.password.data):
			flash("Invalid password")
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
def update_password():
	form = UpdatePasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(user_email=form.email.data).first()
		if not user:
			flash("User does not exists")
			return redirect(url_for("authenticatoion.update_password"))
		
		elif not user.check_password(form.current_password.data):
			print(form.current_password.data)
			flash("Invalid password")
			return redirect(url_for('authentication.update_password'))
	
		flash("Password Updated Sucessfully")
		return redirect(url_for('catalogue.home'))
    			
	return render_template("authentication/update_password.html",form=form)



