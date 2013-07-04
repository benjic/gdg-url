import webapp2

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

		# We set the headers to reflect our response and write raw text.
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Hello, GDG Missoula')

# We define a global SSGIApplication that is used by our configuartion to
# route incoming requests to the App Engine. While we are working we enable
# debugging to promote verbosity.
short_url = webapp2.WSGIApplication([
	('/', RootPage)],
	debug=True)