from bs4 import BeautifulSoup

from ... import helpers

def parse(body):

	try:
		soup = BeautifulSoup(body, "lxml")
	except HTMLParser.HTMLParseError as e:
		return helpers.err(str(e))

	tables = soup.find_all('table')

	# tables[0] == welcome message
	# tables[1] == profile

	if not len(tables) == 2:
		return helpers.err('parse error')

	rows = tables[1].find_all('tr')
	if not len(rows) >= 13:
		return helpers.err('parse error')

	rows = rows[1:] # headers

	data = {}
	"""
		0: name, image
		1: regno
		2: office
		3: course
		4: father name
		5: dob
		6: sex
		7: blood group
		8: address
		9: email
		10: pincode
		11: place of birth
		12: validity
	"""

	try:

		# row 0: name, image
		tds = rows[0].find_all('td')
		name = tds[1].get_text().strip()
		image = tds[2].img['src']

		if image.startswith('../'):
			image = 'http://evarsity.srmuniv.ac.in/srmswi/' + image[3:]

		image = image.strip()

		# row 1: regno
		tds = rows[1].find_all('td')
		regno = tds[1].get_text().strip()

		# row 2: office
		tds = rows[2].find_all('td')
		office = tds[1].get_text().strip()

		# row 3: course
		tds = rows[3].find_all('td')
		course = tds[1].get_text().strip()

		# row 4: father name
		tds = rows[4].find_all('td')
		fname = tds[1].get_text().strip()

		# row 5: dob
		tds = rows[5].find_all('td')
		dob = tds[1].get_text().strip()

		# row 6: sex
		tds = rows[6].find_all('td')
		sex = tds[1].get_text().strip()

		# row 7: blood group
		tds = rows[7].find_all('td')
		bgroup = tds[1].get_text().strip()

		# row 8: address
		tds = rows[8].find_all('td')
		address = tds[1].get_text().strip()

		# row 9: email
		tds = rows[9].find_all('td')
		email = tds[1].get_text().strip()

		# row 10: pincode
		tds = rows[10].find_all('td')
		pincode = tds[1].get_text().strip()

		# row 11: birthplace
		tds = rows[11].find_all('td')
		birthplace = tds[1].get_text().strip()

		# row 12: validity
		tds = rows[12].find_all('td')
		validity = tds[1].get_text().strip()
	except:
		return helpers.err('parse error')

	return helpers.ok({
		'regno': regno,

		'name': name,
		'email': email,
		'image': image,

		'course': course,
		'validity': validity,
		'office': office,

		'dob': dob,
		'sex': sex,
		'bloodgroup': bgroup,
		'fname': fname,

		'address': address,
		'pincode': pincode,
		'birthplace': birthplace,
	})
