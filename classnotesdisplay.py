import os, datetime
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for, jsonify
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

@class_pages.route('/notes/<url_title>/add_assignment', methods=['POST'])
def api_addassignment(url_title):
	
	current_app.logger.info("**** inside assignment ****")
	# return jsonify(request.form)
	honeypot = request.form.get('email')
	
	if request.method == "POST" and honeypot == '':
		entry = models.ClassNote.objects.get(url_title=url_title)
		
		if entry:

			entryData = {
				'name' : request.form.get('name',''),
				'url' : request.form.get('url',''),
				'description' : request.form.get('description','')	
			}

			print "received assignment"
			print entryData
			
			if entryData['name'] != '' and entryData['url'] != '' and entryData['description'] != '':
				assignment = models.Assignment(**entryData)
				entry.assignments.append(assignment)
				entryData['status'] = 'OK'

			else:
				
				entryData = { 'status' : 'ERROR' }

			try:
				entry.save()
				return jsonify(**entryData)
				

			except ValidationError:
				app.logger.error(ValidationError.errors)
				return "error on saving document"
		else:
			abort(500)

	else:
		# no GET on this route
		return "UHOHO"
		# abort(404)/

@class_pages.route('/forum')
def forum():
	return render_template('forum.html')