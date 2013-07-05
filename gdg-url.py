import os
import hashlib

from models import Url

import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/tmpl"),
	extensions=['jinja2.ext.autoescape'])

# Our application must define a request handler for each route defined 
# in the WSGIApplicaiton. RootPage is defined to handle all requests to 
# the root url('/')
class RootPage(webapp2.RequestHandler):
	"""Request handler for root url('/')."""

	# Once a route is matched and the appropriate request handler is called
	# the application calls the appropriate method related to the requests
	# method. GET requests are used as a splash for incoming users.
	def get(self):
		"""Response for GET requests."""

		# When rendering the template we pass a dictionary of values that the
		# template may use. The templates are rendered in a sandbox so local 
		# scope is not applicable. 
		#
		# In this instance the only variable is a conditional flag whether a
		# short url has been created.
		template_values = {
			'created': False,
		}

		template = JINJA_ENVIRONMENT.get_template("root.html")
		self.response.write(template.render(template_values))

	# POST requests are submitted forms for short urls.
	def post(self):
		"""Response for POST requests."""

		# The ideas behind a good hashing algorithm are complex. For
		# this example we will only truncate the first 10 digits of
		# of the md5 hash. This will of course have collisions but it
		# is a problem for another day.
		m = hashlib.md5()
		m.update(self.request.get('link'))

		# The unique hash is truncated to keep our links small.
		url_hash = m.hexdigest()[0:10] 

		# A Url model is instinated with the supplied post data. Our url 
		# shortner uses a hash as a key to recover created urls.
		url = Url(key_name=url_hash,
			link=self.request.get('link'))

		# Model.put() commits the model to the datastore.
		url.put()

		# In this instance the only variable is a conditional flag whether a
		# short url has been created.
		template_values = {
			'created': True,
			'hostname': os.environ.get('HTTP_HOST'),
			'hash': url_hash
		}

		template = JINJA_ENVIRONMENT.get_template("root.html")
		self.response.write(template.render(template_values))

class ShortUrlPage(webapp2.RequestHandler):
	"""Accepts route requests for anything but root."""

	# Requests to a short url should only accept GET http methods.
	def get(self):
		# The request parses the hash from the path by slicing the string to omit
		# the leading "\". We ask the datastore for any entity that matches the hash.
		url = Url.get_by_key_name(self.request.path[1:])

		# If the hash is valid it will return Url Model object else it will return None
		if url:
			# The successul return of a url object allows the application to return a 
			# redirct (301) to the long url.
			self.redirect("http://" + str(url.link))
		else:
			# If there is no short url it is proper to return a 404 as the resource is
			# not available.
			self.abort(404)


# bu define a global SSGIApplication that is used by our configuartion to
# route incoming requests to the App Engine. While we are working we enable
# debugging to promote verbosity.
short_url = webapp2.WSGIApplication([
	('/', RootPage),
	('/.*', ShortUrlPage)],
	debug=True)