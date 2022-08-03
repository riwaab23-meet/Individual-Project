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
		email = request.form.get("email", False)
		password = request.form.get("password", False)
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return render_template("decisions.html")
		except:
			error = "Authentication failed"
			return render_template("signup.html")
	else:
		print("Didn't get to post. got to: {request.method}")
		return render_template("signin.html")
	return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = ""
	if request.method == 'POST':
		first_name = request.form.get("first_name", False)
		last_name = request.form.get("last_name", False)
		email = request.form.get("email", False)
		password = request.form.get("password", False)
		number = request.form.get("number", False)
		birthday = request.form.get("birthday", False)
		bio = request.form.get("bio", False)
		username = request.form.get("username", False)
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			user = {"first_name": first_name,"last_name ":last_name  , "email":email,"password":password, "number": number , "birthday": birthday ,"bio":bio, "username": username   }
			db.child("Users").child(login_session['user']['localId']).set(user)

			return redirect(url_for('decision'))
		except:
			error = "Authentication failed"
			return render_template("signup.html")
	return render_template("signup.html")



if __name__ == '__main__':
	app.run(
		debug = True)