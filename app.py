from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import mysql 

app = Flask(__name__)

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='root',
                       db='Air Ticket Reservation System',
                       charset='utf8mb4',
					   port = 3306,
                       cursorclass=pymysql.cursors.DictCursor)

# mysql = MySQL(app)

app.secret_key="anystringhere"


#Configure
#  MySql 

@app.route('/')
#Home page: 
	#Renders homepage with login and register functionality 
	#Displays current and future flight times
def home():
	
	cursor = conn.cursor()
	query = 'SELECT * from Flight'
	cursor.execute(query)
	data1 = cursor.fetchall()
	for each in data1:
		print(each['flight_number'])
	cursor.close()
	if "username" in session:
		user = session["username"]
		print("In-session")
		return render_template('CustomerHomePage.html', flights=data1, user=user)
	else:
		return render_template('HomePage.html', flights=data1)

#  Search for future flights based on source city/airport name, destination city/airport name, 
# departure date for one way (departure and return dates for round trip)
'''
@app.route('/result', methods = ['POST', 'GET'])
def future_flight():
		cursor = conn.cursor()
		if request.method == 'POST':
    			future_flight = request.form
				leaving = future_flight['Leaving From']
				going =  future_flight['Going To']
				cursor.execute(SELECT Departure_date from Flight WHERE Departure_date > time )
				r=cursor.fetchone()
				conn.commit()
				cursor.close()
				return render_template ("HomePage.html", r=r)




@app.route('/login', methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor()
		cursor.execute('INSERT INTO info_table VALUES(%s,%s),(name,age)')
		mysql.connection.commit()
		cursor.close()
		return "success"
	return render_template('Login.html')
	
'''

#Authenticates the login
@app.route('/login', methods=['GET', 'POST'])
def login():
	#grabs information from the forms
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		print('hello')
		#cursor used to send queries
		cursor = conn.cursor()
		#executes query
		query = 'SELECT * FROM customer WHERE email = %s and password = %s'
		cursor.execute(query, (username, password))
		#stores the results in a variable
		data = cursor.fetchone()
		#use fetchall() if you are expecting more than 1 data row
		cursor.close()

		print(data)
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
	else:
		return render_template('login.html')


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
'''
@app.route('/home')
def home():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall() 
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('home.html', username=username, posts=data1)

'''
@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')


@app.route('/sign-up', methods= ['GET', 'POST'])
def sign_up():
	if request.method == "POST":
		email = request.form.get('firstName')
#Init 
@app.route('/')
def hello():
    return render_template('HomePage.html')
#Define route for login



# @app.route('/login')
# def login():
# 	return render_template('Login.html')


#Define route for register
@app.route('/register')
def register():
	return render_template('Register.html')

@app.route('/profile')
#Load up any flights where id is the same 
#And display them 
def profile():
	username = session['username']
	cursor = conn.cursor()
	#Selects ticket information where username is same and orders it by time
	query = 'SELECT Ticket_id, flight_number, sold_price FROM ticket WHERE username = %s ORDER by date, time desc'
	cursor.execute(query, (username))
	data1 = cursor.fetchall()
	cursor.close()
	return render_template("MyProfile.html")

@app.route('/statistics')
def statistics():
	return render_template("Statistics.html")

@app.route('/payment', methods=['GET', 'POST'])
def payment():
	username = session['username']
	cursor = conn.cursor()
	card_type = request.form['credit/debit']
	card_num = request.form['card_num']
	name_on_card = request.form['card_name']
	exp_date = request.form['exp_date']
	query = 'SELECT * FROM Ticket WHERE username = %s'
	cursor.execute(query, (username))
	data = cursor.fetchone()

	if(data):
		error = 'Payment information already exists'
		return render_template('payment.html', error=error)
	else:
		new_info = 'INSERT INTO ticket VALUES(%s, %s, %s, %s)'
		cursor.execute(new_info, (card_type, card_num, name_on_card, exp_date))
		conn.commit()
		cursor.close()
	return render_template("Payment.html")

#Adds the flight,airport, and airplane
@app.route('/addinfo')
def addinfo():
	return render_template('AddInfo.html')
@app.route('/bookflight')
def bookflight():
	username = session['username']
	return render_template('BookFlight.html')

#Adds confirmation page
@app.route('/confirm')
def confirm():
	return render_template('Finalize.html')

#User authentification
@app.route('/staffprofile')
def staffprofile():
	return render_template("staffprofile.html")
#Register 
@app.route('/staffregister')
def staffregister():
	return render_template("staffregister.html")



if __name__ == "__main__": 
    app.run('127.0.0.1', 5000, debug= True )

