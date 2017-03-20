import requests
import json

def conn(self):
	if self.session:
		return

	# defaults
	self.session = requests.Session()
	self.session.headers.update({
		'origin': "https://academia.srmuniv.ac.in",
		'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
		'cache-control': "no-cache",
	})

	# login
	url1 = 'https://academia.srmuniv.ac.in/accounts/signin.ac'
	payload1 = {
		'client_portal': 'true',
		'grant_type': 'password',
		'is_ajax': 'true',
		'portal': '10002227248',
		'servicename': 'ZohoCreator',
		'serviceurl': 'https://academia.srmuniv.ac.in/',

		'username': self.email,
		'password': self.password,
	}
	r1 = requests.Request('POST', url1, data=payload1)
	p1 = r1.prepare()
	p1.headers.update({
		'referer': "https://academia.srmuniv.ac.in/accounts/signin"
	})

	for i in range(0, self.retries):
		try:
			resp = self.session.send(p1, timeout=self.timeout)
		except requests.exceptions.RequestException as e:
			self.status = e
			if self.debug:
				print(e)
			continue # try again

		j1 = None
		try:
			j1 = resp.json()
		except ValueError as e:
			self.status = e
			if self.debug:
				print(e)
			continue # try again

		if 'error' in j1.keys():
			self.status = json.dumps(j1['error'])
			return # fatal, return.

		# do NOT refactor this
		if 't' in j1.keys() and 'data' in j1.keys():
			if ('success' != j1['data']['response']):
				self.status = "unknown error"
				return # fatal, return.
			else:
				return # normal, status='ok', return
		else:
			self.status = "unknown error"
			return # fatal, return.
