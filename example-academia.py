#!/usr/bin/env python

from academia import academia

payload = {
	'email': 'xxxxxxxxxx@srmuniv.edu.in',
	'password': 'xxxxxxxxxxxx',
	'semester': 4,
}

o = academia.init(payload)
if "ok" == o.status:
	print(o.get('attendance'))
