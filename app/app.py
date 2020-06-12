import os
#from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from objectdetection import ObjectDetction
from datetime import datetime
import flask

DATA_DIR = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = flask.Flask(__name__, static_folder=DATA_DIR)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = DATA_DIR
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		
        
		now = datetime.now() # current date and time

		year = now.strftime("%Y")
		print("year:", year)

		month = now.strftime("%m")
		print("month:", month)

		day = now.strftime("%d")
		print("day:", day)

		time = now.strftime("%H%M%S")
		print("time:", time)

		date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
		print("date and time:",date_time)
        
        
		filename = secure_filename(file.filename)
        
		filename = time + day + month + year + filename
        
        
        
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		print('upload_image filename: ' + filename)
		obj = ObjectDetction("static/uploads/"+filename)
		print("Calling detection")
		obj.identify()
		flash('Image successfully uploaded and displayed')
		

        
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/static/uploads/<filename>')
def display_image(filename):
	print('display_image filename: ' + filename)
	
	return redirect(url_for('static', filename=filename), code=301)

if __name__ == "__main__":
    app.run()
