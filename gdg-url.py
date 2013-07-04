import os

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

# We define a global SSGIApplication that is used by our configuartion to
# route incoming requests to the App Engine. While we are working we enable
# debugging to promote verbosity.
short_url = webapp2.WSGIApplication([
	('/', RootPage)],
	debug=True)