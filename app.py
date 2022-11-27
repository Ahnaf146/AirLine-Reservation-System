from flask import Flask, render_template, request, session, url_for, redirect
#from flask_mysqldb import MySQL

app = Flask(__name__)
'''
app.static_folder = 'static'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '***' # TODO: Change this password
app.config['MYSQL_DB'] = 'Air Ticket Reservation System'
app.config['MYSQL_PORT'] = 3306
'''

# mysql = MySQL(app)


#Configure
#  MySql


'''
Code to connect to mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route('/login', methods = ['POST', 'GET'])
def login():
	if request.method == 'GET':
		return "Login via the login Form"
	if request.method == 'POST':
		name = request.form['name']
		age = request.form['age']
		cursor = mysql.connection.cursor()
		cursor.execute(#INSERT INTO info_table VALUES(%s,%s),(name,age))
		mysql.connection.commit()
		cursor.close()
		return "success"
	return render_template('Login.html')
	
#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO user VALUES(%s, %s)'
		cursor.execute(ins, (username, password))
		conn.commit()
		cursor.close()
		return render_template('MyProfile.html')

@app.route('/home')
def home():
    
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall() 
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('home.html', username=username, posts=data1)

		
@app.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = conn.cursor();
	blog = request.form['blog']
	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
	cursor.execute(query, (blog, username))
	conn.commit()
	cursor.close()
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')


@auth.route('/login', methods= ['GET', 'POST'])
def login():

@auth.route('/sign-up', methods= ['GET', 'POST'] 
def sign_up():
	if request.method == "POST":
		email = request.form.get('firstName')
	


'''

#Init 
@app.route('/')
def hello():
    return render_template('HomePage.html')
#Define route for login

@app.route('/login')
def login():
	return render_template('Login.html')

#Define route for register
@app.route('/register')
def register():
	return render_template('Register.html')

@app.route('/profile')
def profile():
	return render_template("MyProfile.html")

@app.route('/statistics')
def statistics():
	return render_template("Statistics.html")

@app.route('/payment')
def payment():
	return render_template("Payment.html")


if __name__ == "__main__": 
    app.run('127.0.0.1', 5000, debug= True )

