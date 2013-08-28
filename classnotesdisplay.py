import os, datetime
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from jinja2 import TemplateNotFound

import models
from libs.User import User

class_pages = Blueprint('class_pages', __name__, template_folder='templates')

@class_pages.route('/')
def index():
	templateData = {
		'classnotes' : models.ClassNote.objects.order_by("+class_date")
	}
	return render_template('index.html', **templateData)


@class_pages.route('/notes/<url_title>')
def entry_page(url_title):

	# get class notes entry with matching slug
	entry = models.ClassNote.objects.get(url_title=url_title)

	if entry:
		templateData = {
			'entry' : entry
		}
		return render_template('entry.html', **templateData)

	else:
		return "not found"

@class_pages.route('/forum')
def forum():
	return render_template('forum.html')