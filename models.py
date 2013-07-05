import urllib2
from urlparse import urlparse
import logging

from google.appengine.ext import db

class BadUrlError(Exception):
	pass

class ValidLinkProperty(db.LinkProperty):
	"""Url models must validate submitted links."""

	# By overriding the parent validate method we are able to perform
	# url validation before commiting data to the data store.
	def validate(self, value):

		# Our users may submit links in a variety of ways. We will check
		# to determine the link meets a certian level of uniformity with the
		# builtin urlparse library. 
		try:
			# We first try to parse the given value. We then try to fetch the Url
			# for a code.
			url = urlparse(str(value))
			urllib2.urlopen(url.geturl()).getcode()
		except ValueError:
			# In the event that the value is unretriveable it is most likely due to
			# a lack of a scheme when parsed. We inject the default http protocol
			# on the value and recheck and try again.
			try:
				url = urlparse('http://' + str(value))
				urllib2.urlopen(url.geturl()).getcode()
			except:
				# If we recieve any continued errors we give up on the url.
				raise BadUrlError("Your url, " + value + ", has problems we did not anticipate\
					please give it another try.")

		return url.geturl()

class Url(db.Model):
	"""Url models the shortend link."""

	# The link is stored as a string
	link = ValidLinkProperty(required=True)