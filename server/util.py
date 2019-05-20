import requests, os
import filetype
import shutil
import json

def is_downloadable(url):
	h = requests.head(url, allow_redirects=True, verify=False)
	if not h.status_code == 200:
		return False
	header = h.headers
	content_type = header.get('content-type')
	if 'text' in content_type.lower():
		return False
	if 'html' in content_type.lower():
		return False
	return True

def download_file(url, path):
#	path = "./data/"+path
	if not is_downloadable(url):
		return False
	r = requests.Response()
	if not os.path.isfile(path):
		r = requests.get(url, verify=False)
		if r.status_code == 200:
			with open(path, 'wb') as f:
				f.write(r.content)
	kind = filetype.guess(path)
	path = path.replace("∑", ".").replace("§", "\"")
	if kind is not None:
		os.rename(path, path+"."+kind.extension)
#		print('File extension: %s' % kind.extension)
	return True
	

def zip_file(data_path, dir_name):
	path = os.path.join(data_path, dir_name)
	zip_path = os.path.join(data_path, dir_name)
	shutil.make_archive(zip_path, 'zip', path)
	

def write_dict_to_json(data_path, dict, course):
	path = os.path.join(data_path, course)
	with open( path +'.json', 'w') as fp:
		json.dump(dict, fp)
	fp.close()

def read_json_file(path):
	with open(path) as json_file:
		json_data = json.load(json_file)
		return json_data
