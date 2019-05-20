import requests, re, json, os, argparse
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import util

account = "zid"
password = "zPassword"
courseList = ["code"]
csrf_token = ""

#root = "https://webcms3.cse.unsw.edu.au"
url = "https://ssologin.unsw.edu.au/cas/login?service=https://moodle.telt.unsw.edu.au/login/index.php?authCAS=CAS"

data_path = '../data'

dict = {}
client = requests.Session()

#def login(account, password):
#	soup = BeautifulSoup(client.get(url , verify=False).text, "lxml")
#	metas = soup.find_all('meta')
#	for m in metas:
#		if m.get('name') == "csrf-token":
#			csrf_token = m.get('content')
#			
#	cookie = client.cookies.get_dict().get('session')
#	headers = {
#		'Connection':'keep-alive',
#		'Content-Type':'application/x-www-form-urlencoded',
#		'Host': 'webcms3.cse.unsw.edu.au',
#		'Accept-Encoding' :	'br, gzip, deflate',
#		'Cookie': 'session='+cookie,
#		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15'
#	}
#	data = "csrf_token="+ csrf_token +"&zid="+account+"&password="+password
#	r = client.post(url, headers=headers, data=data, verify=False)
#	if "Wrong" in r.text :
#		return False
#	return True
	
def login(account, password):
	soup = BeautifulSoup(client.get(url , verify=False).text, "lxml")
	metas = soup.find_all('input')
	for m in metas:
		if m.get('name') == "lt":
			lt = m.get('value')
	
#	print(lt)
	cookie = client.cookies.get_dict()
	JSESSIONID = cookie.get('JSESSIONID')

	headers = {
		'Connection':'keep-alive',
		'Content-Type':'application/x-www-form-urlencoded',
		'Host': 'ssologin.unsw.edu.au',
		'Accept-Encoding' :	'br, gzip, deflate',
		'Cookie': 'JSESSIONID='+JSESSIONID,
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15'
	}
#	data = "csrf_token="+ csrf_token +"&zid="+account+"&password="+
#	data = {"lt":lt, "_eventId":"submit", "username":account, "password":password, "submit":"Agree and sign on"}
	data = ""
	r = client.post(url, headers=headers, data=data, verify=False)
	print(r.text)
	if "Wrong" in r.text :
		return False
	return True

def download(account_input, password_input, courseList_input):
	account = account_input
	password = password_input
	course = courseList_input
	login(account, password)

login('z5102511', 'Fh5654013')


