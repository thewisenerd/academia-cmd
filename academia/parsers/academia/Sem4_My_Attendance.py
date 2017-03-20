from bs4 import BeautifulSoup

from ... import helpers

def parse(body):

	# delete leading </style>
	# grr
	body = body.strip()
	if body.startswith('</style>'):
		body = body[len('</style>'):]

	try:
		soup = BeautifulSoup(body, "lxml")
	except HTMLParser.HTMLParseError as e:
		return helpers.err(str(e))

	tables = soup.find_all('table')

	# tables[2] == student details
	# tables[3] == attendance

	if not len(tables) == 4:
		return helpers.err('parse error')

	rows = tables[3].find_all('tr')
	rows = rows[1:] # headers

	data = []
	for r in rows:
		col = r.find_all('td')
		# type = "theory, practical, Lab Based Theory"
		# cate = "Core, elective, open elective"
		# 0: cc
		# 1: title
		# 2: type
		# 3: faculty
		# 4: slot
		# 5: room
		# 6: total
		# 7: missed
		# 8: percent

		if not len(col) >= 7:
			return helpers.err('parse error')

		col[0].font.clear(); # clear 'regular' text
		cc = col[0].get_text()
		title = col[1].get_text()
		ctype = col[2].get_text()
		faculty = col[3].get_text()
		slot = col[4].get_text()
		room = col[5].get_text()

		try:
			total = int(col[6].get_text())
			missed = int(col[7].get_text())
		except TypeError as e:
			return helpers.err('parse error')

		data.append({
			'course': {
				'slot': slot,
				'code': cc,
				'title': title,
				'type': ctype,
				'faculty': faculty,
				'room': room,
			},
			'total': total,
			'absent': missed,
			'percent': (total - missed) / total * 100,
		})

	return helpers.ok(data)
