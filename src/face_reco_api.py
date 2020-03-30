import os
import urllib.request
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

from face_recognizer import *
import json


app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_busy():

	with open('src/database.json','r') as json_file:
		data = json.load(json_file)	
	if(data['flag_occupied']=="BUSY"):
		return True
	else:
		with open('src/database.json','w') as json_file:
			data['flag_occupied']="BUSY"
			json.dump(data, json_file)
		return False
	
def not_busy():
	with open('src/database.json','r') as json_file:
		data = json.load(json_file)
	
	with open('src/database.json','w') as json_file:
		data['flag_occupied']="NOT BUSY"
		json.dump(data, json_file)

	print("NOT BUSY")
		


@app.route('/detect_faces/', methods=['POST'])
def upload_file():
	
	if is_busy():	
		resp = jsonify({'message': 'Service is being used'})
		resp.status_code = 400
		return resp

	
	if 'file' not in request.files:
		resp = jsonify({'message': 'No file part in the request'})
		resp.status_code = 400
		not_busy()
		return resp

	file_1 = request.files['file']

	if file_1.filename == '':
		resp = jsonify({'message': 'No file selected for uploading'})
		resp.status_code = 400
		not_busy()
		return resp

	if file_1 and allowed_file(file_1.filename):
		filename = secure_filename(file_1.filename)

		file_1.save(os.path.join("./", filename))
		img=cv2.imread(f"./{filename}")

		detections=do_detect(img)
		print(detections)
		resp = jsonify({'message' : detections})
		resp.status_code = 201
		not_busy()
		return resp

	else:
		resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
		resp.status_code = 400
		not_busy()
		return resp



if __name__ == "__main__":
    app.run(host='0.0.0.0')

    

