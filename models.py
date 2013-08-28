import datetime
from app import db

class User(db.Document):
	email = db.EmailField(unique=True)
	password = db.StringField(default=True)
	active = db.BooleanField(default=True)
	isAdmin = db.BooleanField(default=False)
	timestamp = db.DateTimeField(default=datetime.datetime.now())

class Assignment(db.EmbeddedDocument):
    name = db.StringField(required=True)
    description = db.StringField()
    url = db.StringField()
    github_url = db.StringField()
    timestamp = db.DateTimeField(default=datetime.datetime.now())
    
class ClassNote(db.Document):
    title = db.StringField(required=True,max_length=120)
    url_title = db.StringField(unique=True,required=True, max_length=120)
    description = db.StringField()
    class_date = db.DateTimeField()
    content = db.StringField()
    assignment = db.StringField()
    assignments = db.ListField( db.EmbeddedDocumentField(Assignment) )
    github_url = db.StringField(default=None)
    demo_url = db.StringField(default=None)
    # references = db.ListField( db.EmbeddedDocumentField(Link) )
    last_updated = db.DateTimeField(default=datetime.datetime.now())
    published = db.BooleanField(default=False)
    