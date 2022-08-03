from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
	"apiKey": "AIzaSyAjybNPe3uLUPW48SBWlKJ2dxJvdfUlZDo",
	"authDomain": "meet-adcad.firebaseapp.com",
	"projectId": "meet-adcad",
	"storageBucket": "meet-adcad.appspot.com",
	"messagingSenderId": "748398115568",
	"appId": "1:748398115568:web:07c539a4b68ba470b06035",
	"measurementId": "G-XWDD4KZYPN",
	"databaseURL":""
}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
#db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = ""
	if request.method == 'POST':
		first_name = request.form['first_name']
		last_name = request.form['first_name']
		email = request.form['email']
		password = request.form['password']
		number = request.form['number']
		birthday = request.form['birthday']
		bio = request.form['bio']
		username = request.form['username']



		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			user = {"first_name": first_name,"last_name ":last_name  , "email":email,"password":password, "number": number , "birthday": birthday ,"bio":bio, "username": username   }
			db.child("Users").child(login_session['user']['localId']).set(user)

			return redirect(url_for('decision'))
		except:
			error = "Authentication failed"
			return render_template("decision.html")

	else:
		print("Didn't get to post.")
		return render_template("home.html")



@app.route('/', methods=['GET', 'POST'])
def signin():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('decision'))
		except:
			error = "Authentication failed"
			return render_template("signup.html")
	else:
		print("Didn't get to post. got to: {request.method}")
		return render_template("home.html")
