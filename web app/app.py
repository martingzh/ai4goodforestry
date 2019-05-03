from flask import Flask, render_template, flash, redirect, url_for, session, request
from flaskext.mysql import MySQL
# from flask_uploads import UploadSet, IMAGES, configure_uploads
# from flask_sqlalchemy import SQLAlchemy
from werkzeug.debug import DebuggedApplication

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'XYZ'
app.config['MYSQL_DATABASE_DB'] = 'root@forestry'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# UPLOADS_DEFAULT_DEST = TOP_LEVEL_DIR + '/project/static/img/'
UPLOADS_DEFAULT_URL = 'http://localhost:5000/static/img/'
 
# UPLOADED_IMAGES_DEST = TOP_LEVEL_DIR + '/project/static/img/'
UPLOADED_IMAGES_URL = 'http://localhost:5000/static/img/'

mysql.init_app(app)
 
@app.route("/")
def home():
    return render_template('home.html')

@app.route('/upload', methods= ['POST'])
def upload():
	if request.method == 'POST':
		file = request.files['inputFile']
		file.save(secure_filename(file.filename))
		return file.filename



@app.route('/getall')
def getall():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM example''')
	returnvals = cur.fetchall() #((1, "ID1"), (2, "ID2"),...)
	printthis = ""
	for i in returnvals:
		printthis += i + "<br>"

	return printthis


@app.route("/Authenticate")
def Authenticate():
    password = request.args.get('Password')
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from user where Password='" + password + "'")
    data = cursor.fetchone()
    if data is None:
     return "Password is wrong"
    else:
     return "Logged in successfully"


if __name__ == "__main__":
   app.run(debug = True)    


