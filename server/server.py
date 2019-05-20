from flask import Flask,jsonify, url_for
from flask_restful import reqparse, request
import json
import webcms3

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():	
	code_list = ['COMP9321','COMP9319','COMP2511','COMP9444','COMP1511']
	name_list = ['Data Services Engineering','Web Data Compression and Search','Object-Oriented Design & Programming','Neural Networks and Deep Learning','Introduction to Programming']
	comp9321_url="https://webcms3.cse.unsw.edu.au/static/uploads/coursepic/COMP9321/18s2/1a4f74bd93b3b133abbb68b259a1b426034178501c84233457f1edf7d999a1b5/report-3050965_1280.jpg"
	comp9319_url="https://techhalls.com/wp-content/uploads/2018/06/videoblocks-data-compression-animated-word-cloud-text-design-animation_hs1obcmpl_thumbnail-full02-1200x675.png"
	comp2511_url="https://edward-designer.com/web/wp-content/uploads/2013/09/php8.jpg"
	comp9444_url="https://rossintelligence.com/wp-content/uploads/2018/01/1_vKJ11OU-TiaIJ-2PDawJqQ-1024x724.jpeg"
	comp1511_url="https://i.ytimg.com/vi/rBu_quzdZN4/maxresdefault.jpg"
	url_list = [comp9321_url,comp9319_url,comp2511_url,comp9444_url,comp1511_url]
	json_string = json.dumps([{'Code': code,'Name': name, 'URL': url} for code, name, url in zip(code_list,name_list, url_list)])
	json_dic = json.loads(json_string)
	info = {"status" : "","course": ""}
	info['course']=json_dic
	return jsonify(info)
	

@app.route("/banner", methods=['GET'])
def banner():
	organisation_list = ['ARC','CSE Hackathon','CSE Revue']
	arc_url = "http://bluesat.com.au/wp-content/uploads/2015/11/Arc-Clubs-Logo-White-on-Black.jpg"
	cse_hackathon_url = "https://scontent.fcbr1-1.fna.fbcdn.net/v/t1.0-9/39948242_2029429077090054_8917549650752307200_o.jpg?_nc_cat=0&oh=ef7ffc53f6411268764142c9bb314217&oe=5C2881AD"
	cse_revue_url = "https://scontent.fcbr1-1.fna.fbcdn.net/v/t1.0-9/41774629_2056846387681656_8162016546349121536_o.jpg?_nc_cat=0&oh=c4f363c1a719b8bfc9684b847e6601ae&oe=5C62BDF5"
	url_list =[arc_url,cse_hackathon_url,cse_revue_url]
	json_string = json.dumps([{'Organisation': organisation, 'URL': url} for organisation, url in zip(organisation_list, url_list)])
	json_dic = json.loads(json_string)
	info = {"status" : "","organisation entries": ""}
	info['organisation entries']=json_dic
	return jsonify(info)

@app.route("/detail/<cID>", methods=['GET'])
def detail(cID):
	json = webcms3.get_course_outline('undergraduate',cID, 2018)
	return jsonify(json)

@app.route("/resource/<cID>", methods=['GET'])
def resource(cID):
	json = webcms3.get_leture_resoucre('COMP9319')
	return jsonify(json)

@app.route("/download/<cID>", methods=['GET','POST'])
def download(cID):
    content = request.json
    print(content['zid'], content['zPassword'])
    # result = webcms3.download(content['zid'], content['zPassword'], cID)
    # print(result)
    # return jsonify(result)

if __name__ == "__main__":
	app.config['JSON_AS_ASCII'] = False
	app.debug = True
	app.run()
