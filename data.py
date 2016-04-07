# http://docs.mongoengine.org/guide/defining-documents.html
# http://docs.mongoengine.org/en/latest/apireference.html#module-mongoengine.queryset
# http://stackoverflow.com/questions/10434599/how-can-i-get-the-whole-request-post-body-in-python-with-flask
from mongoengine import *
import datetime
import re

connect('jwfeeds')

# Using one-to-many
class Template(DynamicDocument):	
	head         = StringField()
	body         = StringField()
	foot         = StringField()
	last_updated = DateTimeField(default=datetime.datetime.now)	
	meta         = {'collection': 'templates'}

