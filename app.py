import os
import datetime

from flask import Flask
from flask import render_template
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface

app = Flask(__name__)

# app / database config
app.config.from_object(__name__)
app.config['MONGODB_SETTINGS'] = {'HOST':os.environ.get('MONGOLAB_URI'),'DB': 'dwdfall2013'}
app.config['TESTING'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.debug = True

db = MongoEngine(app) # connect MongoEngine with Flask App
app.session_interface = MongoEngineSessionInterface(db) # sessions w/ mongoengine

class Todo(db.Document):
    title = db.StringField(max_length=60)
    text = db.StringField()
    done = db.BooleanField(default=False)
    pub_date = db.DateTimeField(default=datetime.datetime.now)

@app.route('/')
def hello_world():
	Todo(title='testing123123123').save()
	return render_template('index.html')

    # return 'Hello World!'

if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
