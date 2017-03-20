from ...parsers.evarsity import Sem4_General_Profile
from ... import helpers

def get(self, name):
	if not self.methods:
		return helpers.err('no handlers bind.')

	if name not in self.methods.keys():
		return helpers.err('no such handler bind.')

	urlbase = 'http://5@evarsity.srmuniv.ac.in/srmswi/resource/StudentDetailsResources.jsp?resourceid=';
	url = urlbase + self.methods[name]
	response, e = self.request('GET', url)
	if e: # exception occured
		return helpers.err('network request failed; exception: ' + str(e))

	# status code != 200. uh oh.
	if not response.status_code // 100 == 2:
		return helpers.err('network request failed with status code: ' + response.status_code)

	return self.parsers[name](response.text)

def bind(self, semester):
	if (semester == 4):
		self.methods['profile-general'] = '1';
		self.parsers['profile-general'] = Sem4_General_Profile.parse;
