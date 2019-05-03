from flask import Flask, render_template, flash, redirect, url_for, session, request
from flaskext.mysql import MySQL
# from flask_uploads import UploadSet, IMAGES, configure_uploads
# from flask_sqlalchemy import SQLAlchemy
from werkzeug.debug import DebuggedApplication
from werkzeug.utils import secure_filename
mysql = MySQL()
app = Flask(__name__)

UPLOAD_FOLDER = '/path/to/the/uploads' # must change this to the server database
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'XYZ'
app.config['MYSQL_DATABASE_DB'] = 'root@forestry'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # must change this to the server database

 
@app.route("/")
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

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


