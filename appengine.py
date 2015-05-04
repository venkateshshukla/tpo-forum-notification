import webapp2
import run

class AppEngine(webapp2.RequestHandler):
	def get(self):
		run.run_sequence()
		self.response.write('Executed.')

app = webapp2.WSGIApplication([ ('/run', AppEngine), ], debug=True)
