import os, datetime
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from jinja2 import TemplateNotFound
from app import login_manager, flask_bcrypt
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)

import models
import forms
from libs.User import User

admin_pages = Blueprint('admin_pages', __name__, template_folder='templates')

@login_manager.user_loader
def load_user(id):
	if id is None:

		redirect('/admin/login')

	current_app.logger.info("found user " + id)
	user = User()
	user.get_by_id(id)
	if user.is_active():
		return user
	else:
		return None


@admin_pages.route('/', methods=["GET"])
@login_required
def admin_main():
	entries = models.ClassNote.objects().order_by('+class_date')

	templateData = {
		'entries' : entries
	}	

	return render_template('/admin/index.html', **templateData)


@admin_pages.route('/entry', methods=["GET","POST"])
@login_required
def admin_create_entry():
	if request.method == "POST":

		entryData = {
			'title' : request.form.get('title',''),
			'url_title' : request.form.get('url_title',''),
			'description' : request.form.get('description',''),
			'published' : True if request.form['published'] == "true" else False,
			'github_url' : request.form.get('github_url',None),
			'demo_url' : request.form.get('demo_url',None),
			'content' : request.form.get('content'),
			'assignment' : request.form.get('assignment'),
			'class_date' : datetime.datetime.strptime(request.form.get('class_date'), "%Y-%m-%d")
		}

		entry = models.ClassNote(**entryData)

		try:
			entry.save()
			flash('Class entry:<b>%s</b> was saved' % entry.title)
			return redirect('/admin')

		except ValidationError:
			app.logger.error(ValidationError.errors)
			return "error on saving document"


	return render_template('/admin/entry_new.html')


@admin_pages.route("/admin/entry/edit/<entry_id>", methods=["GET","POST"])
@login_required
def admin_entry_edit(entry_id):
	# get single document returned
	entry = models.ClassNote.objects().with_id(entry_id)
	if entry:
		if request.method == "POST":
			entry.title = request.form.get('title','')
			entry.url_title = request.form.get('url_title','')
			entry.description = request.form.get('description','')
			entry.published = True if request.form['published'] == "true" else False
			entry.github_url = request.form.get('github_url',None)
			entry.demo_url = request.form.get('demo_url',None)
			entry.content = request.form.get('content')
			entry.assignment = request.form.get('assignment')
			entry.class_date = datetime.datetime.strptime(request.form.get('class_date'), "%Y-%m-%d")

			entry.save()


		return render_template('/admin/entry_edit.html', entry=entry)

	else:
		return "Unable to find entry %s" % entry_id		

@admin_pages.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "email" in request.form:
        email = request.form["email"]
        userObj = User()
        user = userObj.get_by_email_w_password(email)
     	if user and flask_bcrypt.check_password_hash(user.password,request.form["password"]) and user.is_active():
			remember = request.form.get("remember", "no") == "yes"

			if login_user(user, remember=remember):
				flash("Logged in!")
				return redirect(request.args.get("next") or '/admin')
			else:
				flash("unable to log you in")

    return render_template("/auth/login.html")

#
# Route disabled - enable route to allow user registration.
#
@admin_pages.route("/register", methods=["GET","POST"])
def register():
	
	registerForm = forms.SignupForm(request.form)
	current_app.logger.info(request.form)

	if request.method == 'POST' and registerForm.validate() == False:
		current_app.logger.info(registerForm.errors)
		return "no"

	elif request.method == 'POST' and registerForm.validate():
		email = request.form['email']
		
		# generate password hash
		password_hash = flask_bcrypt.generate_password_hash(request.form['password'])

		# prepare User
		user = User(email,password_hash)
		print user

		try:
			user.save()
			if login_user(user, remember="no"):
				flash("Logged in!")
				return redirect(request.args.get("next") or url_for("index"))
			else:
				flash("unable to log you in")

		except:
			flash("unable to register with that email address")
			app.logger.error("Error on registration - possible duplicate emails")

	# prepare registration form			
	# registerForm = RegisterForm(csrf_enabled=True)
	templateData = {

		'form' : registerForm
	}

	return render_template("/auth/register.html", **templateData)

@admin_pages.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("admin_main"))
    
    templateData = {}
    return render_template("/auth/reauth.html", **templateData)


@admin_pages.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect('/admin/login')