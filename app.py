import os

from flask import Flask  # etc.
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt

app = Flask("dwdfall2013")

app.config['MONGODB_SETTINGS'] = {'HOST':os.environ.get('MONGOLAB_URI'),'DB': 'dwdfall2013'}
app.config['TESTING'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
if os.environ.get('DEBUG'):
	app.debug = True

db = MongoEngine(app) # connect MongoEngine with Flask App
app.session_interface = MongoEngineSessionInterface(db) # sessions w/ mongoengine

# Flask BCrypt will be used to salt the user password
flask_bcrypt = Bcrypt(app)

# flask login manager
login_manager = LoginManager()
login_manager.init_app(app)
