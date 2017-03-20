from .handlers.academia import ConnHandler
from .handlers.academia import AppHandlers

from . import helpers

class Academia(object):
	status = None
	email = None
	password = None
	semester = None
	session = None
	timeout = (2, 2)
	retries = 5
	debug = True
	methods = {}
	parsers = {}

	def __init__(self, payload):
		keys = payload.keys()

		if 'email' not in keys:
			self.status = "Missing email in payload"
			return

		if not any(x in keys for x in ['pass', 'password']):
			self.status = "Missing password in payload"
			return

		if not any(x in keys for x in ['sem', 'semester']):
			self.status = "Missing semester in payload"
			return

		# set email
		self.email = payload['email']

		# set pass
		if 'pass' in keys:
			self.password = payload['pass']
		else:
			self.password = payload['password']

		# set semester
		if 'sem' in keys:
			self.semester = payload['sem']
		else:
			self.semester = payload['semester']

		# ref status
		self.status = "ok"

		# connect
		ConnHandler.conn(self)
		if "ok" != self.status:
			return

		# register handlers
		AppHandlers.bind(self, self.semester)

	def request(self, method, url, payload=None, stream=False):
		return helpers.request(self, method, url, payload, stream)

	def get(self, name):
		return AppHandlers.get(self, name)

# wrapper
def init(payload):
	return Academia(payload);
