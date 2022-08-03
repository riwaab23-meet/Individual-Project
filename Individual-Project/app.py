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
	"databaseURL":"https://console.firebase.google.com/project/meet-adcad/database/meet-adcad-default-rtdb/data/~2F"
}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key' 

@app.route('/')
def hello_name_route():
    return render_template('home.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
	error = ""
	if request.method == 'POST':
		email1 = request.form.get("emailq1", False)
		password1= request.form.get("password1", False)
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email1, password1)
			return render_template("decisions.html")
		except:
			error = "Authentication failed"
			return render_template("signin.html")

	return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = ""
	if request.method == 'POST':
		print("RERFGHJ")
		email = request.form.get("email",False)
		password = request.form.get("password",False)
		username = request.form.get("txt",False)
		try:
			print("1234567")
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			user = { "email":email,"password":password, "username": username   }
			db.child("Users").child(login_session['user']['localId']).set(user)

			return redirect(url_for('decision'))
		except:
			error = "Authentication failed"
			return render_template("signup.html")
	return render_template("signup.html")



if __name__ == '__main__':
	app.run(
		debug = True)