import os
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img,img_to_array
#from flask_ngrok import run_with_ngrok
import numpy as np

UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
model=load_model("mod2.hdf5")
app = Flask(__name__)
#run_with_ngrok(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict(img):
	img  = load_img(img, target_size=(224,224))
	img = img_to_array(img)/255.0
	img = np.expand_dims(img, axis=0)
	probs = model.predict(img)
	#print(type(probs))
	return(probs[0])

@app.route('/result <pred0> <pred1> <pred2> <img>', methods=['GET', 'POST'])
def result(pred0,pred1,pred2,img):

	if request.method == 'POST':
		return redirect(url_for('upload_file'))
	img=os.path.join(app.config['UPLOAD_FOLDER'],img)
	pred0=round(float(pred0),3)*100
	pred1=round(float(pred1),3)*100
	pred2=round(float(pred2),3)*100
	return render_template('result1.html',p0=pred0,p1=pred1,p2=pred2,image=img)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			#filename=os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			l=predict(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('result',pred0=l[0],pred1=l[1],pred2=l[2],img=filename))
			#redirect(request.url)
	return render_template("home.html")

if __name__ == '__main__':
	app.run(debug=True)