from flask import Flask, flash, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, AdminRegisterForm, RegisterForm
from flask_login import (LoginManager, UserMixin, current_user, login_user, logout_user)
from flask_bcrypt import Bcrypt

import string
import random
import json

app = Flask(__name__)

app.config["SECRET_KEY"] = "081a91839fd7bd70282d24fd718f4ca2"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:hgfjffdhb@localhost/db" #"sqlite:///site.db" 

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique= True, nullable=False)
	user_email = db.Column(db.String(100), unique= True, nullable=False)
	password = db.Column(db.String(100), nullable=False)
	is_admin = db.Column(db.Boolean, unique=False, default=False)

	def __repr__(self):
		return f"User({self.id}, {self.username}, {self.user_email}, {self.password}, {self.is_admin})"

class Provision(db.Model):
	prov_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, nullable=False)
	value = db.Column(db.Integer, nullable=False)
	client_name = db.Column(db.String(20))

	def __repr__(self):
		return f"Provision({self.prov_id}, {self.user_id}, {self.value}, {self.client_name})"

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
	if not current_user.is_authenticated:
		return redirect(url_for("login"))

	provisions = Provision.query.all()
	return render_template("dashboard.html", provisions=provisions, current_user=current_user)

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated: 
		return redirect(url_for("dashboard"))

	form = LoginForm()
	if form.validate_on_submit():  
		#hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
		found_matching_credentials = False
		for db_account in User.query.filter_by(username=form.username.data).all():
			if(db_account.username == form.username.data and bcrypt.check_password_hash(db_account.password, form.password.data)):
				found_matching_credentials = True
				break

		if(found_matching_credentials):
			login_user(db_account)
			flash(f"logged in as {form.username.data}", "success")   
			return redirect(url_for("dashboard"))              
		
		else:
			flash("Wrong username or password", "danger")

	return render_template("login.html", form=form)

@app.route("/logout")
def logout():
	logout_user()
	flash(f"you have been logged out", "info")
	return redirect(url_for("login"))


@app.route("/admin_register", methods=["GET", "POST"])
def admin_register():
	if not current_user.is_authenticated:
		return redirect(url_for("login"))

	form = AdminRegisterForm()
	if form.validate_on_submit():

		admin = False
		if form.rights.data == "admin":
			admin = True

		pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
		new_user = User(username=form.username.data, password=pw, user_email=form.user_email.data, is_admin=admin)
		db.session.add(new_user)
		db.session.commit()
		flash(f"successfully created new user {form.username.data}", "success")

	elif "submit" in request.form:
		for fieldName, errorMessages in form.errors.items():
			for error in errorMessages:
				flash(f"Benutzerregistrierung ({fieldName}): {error}", "danger")

	lower = string.ascii_lowercase
	upper = string.ascii_uppercase
	num = string.digits
	symbols = string.punctuation

	all = lower + upper + num + symbols
	temp = random.sample(all, 12)
	recommended_pw = "".join(temp)

	return render_template("admin_register.html", form=form, recommended_pw=recommended_pw)

@app.route("/register", methods=["GET", "POST"])
def register():

	form = RegisterForm()
	if form.validate_on_submit():
		pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

		new_user = User(username=form.username.data, password=pw, user_email=form.user_email.data, is_admin=0)
		db.session.add(new_user)
		db.session.commit()
		flash(f"successfully created new user {form.username.data}", "success")
		return redirect(url_for("login"))

	elif "submit" in request.form:
		for fieldName, errorMessages in form.errors.items():
			for error in errorMessages:
				flash(f"Benutzerregistrierung ({fieldName}): {error}", "danger")
				
	lower = string.ascii_lowercase
	upper = string.ascii_uppercase
	num = string.digits
	symbols = string.punctuation

	all = lower + upper + num + symbols
	temp = random.sample(all, 12)
	recommended_pw = "".join(temp)

	return render_template("register.html", form=form, recommended_pw=recommended_pw)

@app.route("/api/<user_id>", methods=["GET"])
def api(user_id):
	prov_dict = {}
	provisions = Provision.query.filter_by(user_id=user_id).all()
	for prov in provisions:
		prov_dict[prov.client_name] = prov.value

	return str(json.dumps(prov_dict))


if __name__ == "__main__":   
	app.run(debug=True)
