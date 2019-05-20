import requests, re, json, os, argparse
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import util

account = "zid"
password = "zPassword"
courseList = ["code"]
csrf_token = ""

root = "https://webcms3.cse.unsw.edu.au"
url = "https://webcms3.cse.unsw.edu.au/login"

data_path = '../data'

dict = {}
client = requests.Session()

def login(account, password):
	soup = BeautifulSoup(client.get(url , verify=False).text, "lxml")
	metas = soup.find_all('meta')
	for m in metas:
		if m.get('name') == "csrf-token":
			csrf_token = m.get('content')
			
	cookie = client.cookies.get_dict().get('session')
	headers = {
		'Connection':'keep-alive',
		'Content-Type':'application/x-www-form-urlencoded',
		'Host': 'webcms3.cse.unsw.edu.au',
		'Accept-Encoding' :	'br, gzip, deflate',
		'Cookie': 'session='+cookie,
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15'
	}
	data = "csrf_token="+ csrf_token +"&zid="+account+"&password="+password
	r = client.post(url, headers=headers, data=data, verify=False)
	if "Wrong" in r.text :
		return False
	return True

def download_lecture_notes(course):
	print("  -------------  Start downloading "+course+"'s Lecture  -------------  ")
	url = "https://webcms3.cse.unsw.edu.au/"+ course +"/18s2"
	r = client.get(url, verify=False)
	if not r.status_code == 200:
		return print("")
	soup = BeautifulSoup(r.text, "lxml")
	sider_bar = soup.find('div', id='sidebar')
	lec = sider_bar.find('a', string="Lectures")
	if not lec:
		lec = sider_bar.find('a', string="Lectures  ")
	location = lec['href']

	url_lec = root + location
	r = client.get(url_lec, verify=False)
	soup = BeautifulSoup(r.text, "lxml")
	blocks = soup.find_all('div', 'panel panel-primary')
	dict[course]["lec"] = {}
	
#	print(sider_bar)
	
	for block in blocks:
		week_str = block.h4.text.strip()
		small = block.h4.small.text.strip()
		week_str = week_str.replace(small, "")
		week_str = week_str.replace("active", "")
		week_str = re.sub(r'\n', "", week_str)
		week_str = " ".join(week_str.split())
		week_str = week_str.strip()
		dict[course]["lec"][week_str] = {}
		
		path = os.path.join(data_path, course, week_str)
		if not os.path.exists(path):
			os.makedirs(path)
		
		items = block.find_all('li','list-group-item')
		for item in items:
			name = item.find('a').text.strip()
			if len(name) <=0:
				continue
			name = " ".join(name.split())
			
			pdf = item.div.find('a',title="Download")
			pdf_url = root
			if pdf:
				pdf_url = root + pdf.get('href')
			if pdf_url == root:
				pdf_url = item.div.a.get('href')
			
			if pdf_url != root:
				name = name.replace("/", " ")
				path = os.path.join(data_path, course, week_str, name)
#				path = path.replace("\"", "§")
				succ = util.download_file(pdf_url, path)
				name = name.replace(".","&")
				dict[course]["lec"][week_str][name]=pdf_url
			else:
				print("Cannot find lecture pdf")


	print("  -------------  Lecture download complete. :^ )  -------------  ")
	
def download_lab(course):
	print("  -------------  Start downloading "+course+"'s Lab  -------------  ")
	url = "https://webcms3.cse.unsw.edu.au/"+ course +"/18s1"
	r = client.get(url, verify=False)
	soup = BeautifulSoup(r.text, "lxml")
	### Lab Activities, Labs
	sider_bar = soup.find('div', id='sidebar')
	lab = sider_bar.find('a', string=re.compile('Lab'))
	if not lab:
		print(course + " may not have Lab")
		return
	location = lab['href']

	url_lec = root + location
	r = client.get(url_lec, verify=False)
	soup = BeautifulSoup(r.text, "lxml")
	blocks = soup.find_all('div', 'panel panel-primary')
	dict[course]["lab"] = {}

	for block in blocks:
		week_str = block.h4.text.strip()
		small = block.h4.small.text.strip()
		week_str = week_str.replace(small, "")
		week_str = week_str.replace("active", "")
		week_str = re.sub(r'\n', "", week_str)
		week_str = " ".join(week_str.split())
		week_str = week_str.strip()
		dict[course]["lab"][week_str] = {}
		
		path = os.path.join(data_path, course, week_str, "lab")
		if not os.path.exists(path):
			os.makedirs(path)
		
		items = block.find_all('li','list-group-item')
		for item in items:
			name = item.find('a').text.strip()
			if len(name) <=0:
				continue
			name = " ".join(name.split())
			
			pdf = item.div.find('a',title="Download")
			if pdf:
				pdf_url = root + pdf.get('href')
				path = os.path.join(data_path, course, week_str, "lab",name)
				path.replace("\"", "§")
				succ = util.download_file(pdf_url, path)
				name = name.replace(".","&")
				dict[course]["lab"][week_str][name] = pdf_url
	print("  -------------  Lab download complete. :^ )  -------------  ")

def download_asst(course):
	print("  -------------  Start downloading "+course+"'s Asst  -------------  ")
	url = "https://webcms3.cse.unsw.edu.au/"+ course +"/18s1"
	r = client.get(url, verify=False)
	soup = BeautifulSoup(r.text, "lxml")
	#### Assignments Assessments
	sider_bar = soup.find('div', id='sidebar')
	asst = sider_bar.find('a', string=re.compile('Ass'))
#	print(asst)
	if not asst:
		print(course + " may not have Asst")
		return
	location = asst['href']

	url_lec = root + location
	r = client.get(url_lec, verify=False)
	soup = BeautifulSoup(r.text, "lxml")
	blocks = soup.find_all('div', 'panel panel-primary')
	dict[course]["asst"] = {}

	for block in blocks:
		week_str = block.h4.text.strip()
		small = block.h4.small.text.strip()
		week_str = week_str.replace(small, "")
		week_str = week_str.replace("active", "")
		week_str = re.sub(r'\n', "", week_str)
		week_str = " ".join(week_str.split())
		week_str = week_str.strip()
		dict[course]["asst"][week_str] = {}
		
		path = os.path.join(data_path, course, week_str)
		if not os.path.exists(path):
			os.makedirs(path)
		
		items = block.find_all('li','list-group-item')
		for item in items:
			name = item.find('a').text.strip()
			if len(name) <=0:
				continue
			name = " ".join(name.split())
			
			pdf = item.div.find('a',title="Download")
			if pdf:
				pdf_url = root + pdf.get('href')
				path = os.path.join(data_path, course, week_str,name)
				path.replace("\"", "§")
				succ = util.download_file(pdf_url, path)
				name = name.replace(".","&")
				dict[course]["asst"][week_str][name] = pdf_url
	print("  -------------  Asst download complete. :^ )  -------------  ")

def get_course_outline(degree,course,year):
	url = "http://legacy.handbook.unsw.edu.au/{}/courses/{}/{}.html".format(degree,year,course)
	print(url)
	r = requests.get(url)
	if r.status_code==200:
		soup = BeautifulSoup(r.text,"lxml")
		for div in soup.findAll('div', attrs={'class':'internalContentWrapper'}):
			content = div.text
			campus = content.split("Campus:",1)[1]
			campus = campus.split('Career', 1)[0]
                #remove the white space in the front and back
			campus = campus.strip()
			career = content.split("Career:",1)[1]
			career = career.split('Units of Credit', 1)[0]
			career = career.strip()
			
			uoc = content.split("Units of Credit:",1)[1]
			uoc = uoc.split('EFTSL', 1)[0]
			uoc = uoc.strip()
			
			name = div.h1.text.split('-')[0]
			
			des = content.split("Description",1)[1] 
			des = des.strip()
			
			data = {"Campus" : "","Career": "","Units of Credit":"","Enrolment Requirements" : "","Equivalent":"","Description": "", "Code":""}
			data['Campus']=campus
			data['Career']=career
			data['Units of Credit']=uoc
			data['Code'] = course
			data['Name']=name
			data['Description']=des
			return data


def download(account_input, password_input, courseList_input):
	
	account = account_input
	password = password_input
	course = courseList_input
	
	if not login(account, password):
		print("Login Failed")
		return ""
	else:
		path = os.path.join(data_path,course)
		if os.path.exists(path):
			return path+".zip"
		
		dict[course] = {}
		download_lecture_notes(course)
		util.zip_file(data_path,course)
		zip_filename = course+".zip"
		util.write_dict_to_json(data_path, dict, courseList_input)
		path = os.path.join(data_path, zip_filename)
		return {"link:":path}
		

def get_leture_resoucre(course):
	path = os.path.join(data_path,course)
	path += ".json"
	if os.path.exists(path):
		return util.read_json_file(path)
	############ TODO ###############
	
		
#print()
#get_course_outline('undergraduate','COMP9319', 2018)



