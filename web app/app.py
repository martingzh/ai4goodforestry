from flask import Flask, render_template, flash, redirect, url_for, session, request
from flaskext.mysql import MySQL
# from flask_uploads import UploadSet, IMAGES, configure_uploads
# from flask_sqlalchemy import SQLAlchemy
from werkzeug.debug import DebuggedApplication
from werkzeug.utils import secure_filename
import urllib
from classification import Classify

import os
mysql = MySQL()
app = Flask(__name__)

UPLOAD_FOLDER = '/Users/Jiwon/Desktop/ai4goodforestry/folder' # must change this to the server database
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'XYZ'
app.config['MYSQL_DATABASE_DB'] = 'root@forestry'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # must change this to the server database

 
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/handleUpload", methods=['POST'])
def handleFileUpload():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':            
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return file.filename + " successfully uploaded"

@app.route("/predict", methods=['GET'])
def predictInDis():
    #Get docId from home.html
    #get corresponding document       
    country = request.args.get('country')
    language = request.form.get('language')
    indismot = request.form.get('indismot')

    print(country, language, indismot)

    # answer = Classify(document,classify_india,classify_mexico,is_incentive,is_disincentive,is_motivation)
    return "answer"

@app.route('/getall')
def getall():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM example''')
	returnvals = cur.fetchall() #((1, "ID1"), (2, "ID2"),...)
	printthis = ""
	for i in returnvals:
		printthis += i + "<br>"
	return printthis

if __name__ == "__main__":
   app.run(debug = True)    


