from google.appengine.ext import db

class Url(db.Model):
	"""Url models the shortend link."""

	# The link is stored as a string
	link = db.StringProperty(required=True)