from ...parsers.academia import Sem4_My_Attendance
from ... import helpers

def get(self, name):
	if not self.methods:
		return helpers.err('no handlers bind.')

	if name not in self.methods.keys():
		return helpers.err('no such handler bind.')


	url = 'https://academia.srmuniv.ac.in/liveViewHeader.do';
	payload = {
		'sharedBy': 'srm_university',
		'appLinkName': 'academia-academic-services',
		'urlParams': '{}',
		'isPageLoad': 'true',

		'viewLinkName': self.methods[name],
	}
	response, e = self.request('POST', url, payload=payload)
	if e: # exception occured
		return helpers.err('network request failed; exception: ' + str(e))

	# status code != 200. uh oh.
	if not response.status_code // 100 == 2:
		return helpers.err('network request failed with status code: ' + response.status_code)

	return self.parsers[name](response.text)

def bind(self, semester):
	if (semester == 4):
		self.methods['attendance'] = 'My_Attendance';
		self.parsers['attendance'] = Sem4_My_Attendance.parse;
