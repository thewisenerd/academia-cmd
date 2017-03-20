#!/usr/bin/env python

import json

import requests
import shutil
import tempfile

from academia import evarsity

payload = {
	'regno': 'RA151100xxxxxxx',
	'password': 'xxxxxxxxxxxx',
	'semester': 4,
}

o = evarsity.init(payload)
if "ok" == o.status:
	data = o.get('profile-general')
	if 'ok' == data['status']:
		print(json.dumps(data['data'], indent=2))

		# store user image example
		rq, e = o.request('GET', data['data']['image'], stream=True)
		if e: # exception occured
			print('network request failed; exception: ' + str(e))
		else:
			rq.raw.decode_content = True
			fh = tempfile.NamedTemporaryFile(delete = False)
			shutil.copyfileobj(rq.raw, fh)
			fh.close()
			print('profile image saved at: ' + fh.name)

	else:
		print('error: ' + data['data'])
else:
	print('error: ' + o.status)
