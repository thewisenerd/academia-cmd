import requests
import json

# ocr
from PIL import Image
import pytesseract

# regex
import re

def conn(self):
	if self.session:
		return

	# defaults
	self.session = requests.Session()
	self.session.headers.update({
		'origin': "http://evarsity.srmuniv.ac.in",
		'referer': "http://evarsity.srmuniv.ac.in/srmswi/usermanager/youLogin.jsp",

		'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
	})

	# login payload
	payload1 = {
		'Searchtext1:txtSearchText' : 'Search',
		'txtRegNumber': 'iamalsouser',
		'txtPwd': 'thanksandregards',
		# 'txtverifycode': 'xxxxxx',
		'txtPA': '1',

		'txtSN': self.regno,
		'txtPD': self.password,
	}

	# login
	# scrape login page for session init
	url1 = 'http://evarsity.srmuniv.ac.in/srmswi/usermanager/youLogin.jsp'
	for i in range(0, self.retries):
		try:
			r1 = self.session.request('GET', url1, timeout=self.timeout);
		except requests.exceptions.RequestException as e:
			self.status = e
			if self.debug:
				print(e)
			continue # try again

		if not r1.status_code // 100 == 2:
			self.status = 'network request failed with status code: ' + r1.status_code
		else:
			self.status = "ok"
			break

	if "ok" != self.status:
		return

	for i in range(0, self.retries):
		# get captcha
		url2 = 'http://evarsity.srmuniv.ac.in/srmswi/Captcha'
		try:
			r2 = self.session.get(url2, stream=True)
		except requests.exceptions.RequestException as e:
			self.status = e
			if self.debug:
				print(e)
			continue # try again
		r2.raw.decode_content = True

		# try captcha
		captcha = pytesseract.image_to_string(Image.open(r2.raw));
		payload1['txtverifycode'] = captcha

		# moment of truth
		try:
			r3 = self.session.request('POST', url1, data=payload1, timeout=self.timeout)
		except requests.exceptions.RequestException as e:
			self.status = e
			if self.debug:
				print(e)
			continue # try again

		if 'http://evarsity.srmuniv.ac.in/srmswi/usermanager/youLogin.jsp' == r3.url: # login failed
			regex = r"(?:LoadLoginPage\(\)\{?)([^\}]*)(?:\}?)"
			m1 = re.search(regex, r3.text)
			if not m1:
				self.status = "login failure, unknown error"
				return

			regex = r"loginerror=([^;\"]*)"
			m2 = re.search(regex, m1.group(1))
			if not m2:
				self.status = "login failure, unknown error"
				return

			self.status = m2.group(1) #failure
			if self.debug:
				print(m2.group(1))

			if not (self.status == 'Invalid Verification code'):
				return

		elif 'http://evarsity.srmuniv.ac.in/srmswi/usermanager/home.jsp' == r3.url: # login success
			self.status = "ok"
			break
		else:
			self.status = "login failure, unknown error"
			return

	# update headers
	del self.session.headers['origin']
	del self.session.headers['referer']
	self.session.headers.update({
		'host': "evarsity.srmuniv.ac.in",
		'referer': "http://evarsity.srmuniv.ac.in/srmswi/usermanager/home.jsp",
	})
