import json

def err(data):
	return {
		'status': "err",
		'data': data
	}

def ok(data):
	return {
		'status': "ok",
		'data': data
	}

def request(self, method, url, payload=None, stream=False):
	if self.debug:
		print('.request(' + method + ', ' + url + ');')
		if payload:
			print('\tpayload: ' + json.dumps(payload))
		if stream:
			print('\tstream: ' + str(stream))

	try:
		if not payload:
			response = self.session.request(method, url, timeout=self.timeout, stream=stream)
		else:
			response = self.session.request(method, url, data=payload, timeout=self.timeout, stream=stream)
	except requests.exceptions.RequestException as e:
		if self.debug:
			print(e)
		return (None, e)

	return (response, None)
