from flask import Flask, render_template, request, session, url_for, redirect
import bcrypt
import pymysql.cursors
import mysql

app = Flask(__name__)

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='root',
                       db='Air Ticket Reservation System',
                       charset='utf8mb4',
                       port = 8889,
                       cursorclass=pymysql.cursors.DictCursor)

# mysql = MySQL(app)

app.secret_key="anystringhere"


#HOME PAGE
# Search for future flights based on source city/airport name, destination city/airport name, 
# departure date for one way (departure and return dates for round trip)
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
    if "customer" in session:
        user = session["customer"]
        print("In-session customer")
        return render_template('CustomerHomePage.html', user=user , flights=data1)
    if "staff" in session:
        user = session["staff"]
        print("In-session staff")
        return render_template('StaffHomePage.html', user=user , flights=data1)
    else:
        return render_template('HomePage.html', flights=data1)
    
#CUSTOMER LOGIN PAGE AND LOGOUT 
@app.route('/login', methods=['GET', 'POST'])
def login():
    #grabs information from the forms
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #cursor used to send queries
        cursor = conn.cursor()
        #executes query
        query = 'SELECT password FROM customer WHERE email = %s'
        cursor.execute(query, (username))
        #stores the results in a variable
        data = cursor.fetchone()
        #use fetchall() if you are expecting more than 1 data row
        cursor.close()
        error = None
        if bcrypt.checkpw(password.encode('utf8'), data['password'].encode('utf8')):
            session['customer'] = username
            return redirect(url_for('home'))
        else:
            #returns an error message to the html page
            error = 'Invalid login or username'
            return render_template('Login.html', error=error)
    else:
        return render_template('Login.html')

#STAFF LOGIN PAGE 
@app.route('/loginstaff', methods= ['GET', 'POST'])
def staff_login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        cursor = conn.cursor()
        #executes query
        query = "SELECT password FROM airlinestaff WHERE Username=%s"
        cursor.execute(query,(username))
        #stores the results in a variable
        data = cursor.fetchone()
        #use fetchall() if you are expecting more than 1 data row
        cursor.close()
        error = None
        if bcrypt.checkpw(password.encode('utf8'), data['password'].encode('utf8')):
            session['staff'] = username
            return redirect(url_for('home'))
        else:
        #returns an error message to the html page
            error = 'Invalid login or username'
            return render_template('StaffLogin.html', user=username, error=error)
    else:
        return render_template("StaffLogin.html")


@app.route('/logout')
def logout():
    if "customer" in session:
        session.pop('customer')
    if "staff" in session:
        session.pop('staff')
    message = 'You have been logged out'
    return render_template('HomePage.html', message=message)



#REGISTER FOR NEW USER
#Authenticates the register
#Authenticates the register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #grabs information from the forms
        username = request.form.get('email')
        password = request.form.get('password')
        fullname = request.form.get('fname')
        building_num = request.form.get('building_num')
        street = request.form.get('street')
        City = request.form.get('city')
        State = request.form.get('State')
        passport = request.form.get('passport')
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        #cursor used to send queries
        cursor = conn.cursor()
        #executes query
        query = 'SELECT * FROM customer WHERE email = %s'
        cursor.execute(query, (username))
        #stores the results in a variable
        data = cursor.fetchone()
        #use fetchall() if you are expecting more than 1 data row
        error = None
        if(data):
            #If the previous query returns data, then user exists
            error = "This user already exists"
            return render_template('Register.html', error = error)
        else:
            ins = 'INSERT INTO customer VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

            cursor.execute(ins, (username, fullname, hashed, building_num, street, City, State, passport))
            conn.commit()
            cursor.close()
            session['customer'] = username
            return redirect(url_for('home'))
    else:
        return render_template('Register.html')

#FLIGHT INFORMATION 


#USER PROFILE
@app.route('/profile')
#Load up any flights where id is the same 
#And display them 
def profile():
    user = session['username']
    cursor = conn.cursor()
    #Selects ticket information where username is same and orders it by time
    query = 'SELECT Ticket_id, flight_number, sold_price FROM ticket NATURAL JOIN Customer WHERE Customer.EMAIL = %s AND Customer.EMAIL = ticket.EMAIL'
    cursor.execute(query, (user))
    data1 = cursor.fetchall()
    cursor.close()
    return render_template("MyProfile.html", info = data1, user=user)



#STAFF INFO 

#STAFF Profile
@app.route('/staffprofile')
def staffprofile():
    username = session['staff'] 
    cursor = conn.cursor()
    #Selects all of airline staff flights
    query = 'SELECT * FROM FLIGHT NATURAL JOIN AirlineStaff WHERE AirlineStaff.Airline_name = Flight.Airline_name'
    cursor.execute(query)
    data1 = cursor.fetchall()
    return render_template("staffprofile.html", staffuser = username, staff_flights=data1)

@app.route('/staffview')
#View flight ratings, frequent customers, reports, earned revenue
def staffview():
    username = session['staff']
    cursor= conn.cursor()
    return render_template("StaffView.html", user=username)

@app.route('/staffedit')
def staffedit():
    username = session['staff']
    cursor = conn.cursor()
    return render_template("StaffEdit.html", user=username)

@app.route('/staffregister', methods= ['GET', 'POST'])
def staffregister():
    if request.method == "POST":
        name = request.form.get('name')
        username = request.form.get('username')
        password= request.form.get('password')
        dob = request.form.get('dob')
        phone_num = request.form.get('phone_num')
        airline_name= request.form.get('Airline_name')

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor = conn.cursor()
        query = 'SELECT * from AirlineStaff WHERE Username= %s'
        cursor.execute(query, (username))
        data = cursor.fetchone()
        error = None
        if(data):
            error = "This user already exists"
            return render_template("staffregister.html", error=error)
        else:
            cursor = conn.cursor()
            query = 'SELECT * from airline WHERE airline_name= %s'
            cursor.execute(query, (airline_name))
            data1 = cursor.fetchone()
            if(data1):
                ins = 'INSERT INTO AirlineStaff VALUES(%s, %s, %s, %s, %s, %s)'
                cursor.execute(ins, (username, hashed, name, dob, phone_num, airline_name))
                conn.commit()
                cursor.close()
                session['staff'] = username
                return redirect(url_for('home'))
            else:
                error = "The entered airline does not exist. Please enter a valid airline"
                return render_template("staffregister.html", error=error)
    else:
        return render_template('staffregister.html')
#Adds the flight,airport, and airplane
@app.route('/addinfo', methods= ['GET', 'POST'])
def addinfo():
    username = session['username']
    cursor = conn.cursor()
    #Select current flights 
    query = 'SELECT * from Flight' 
    cursor.execute(query)
    data = cursor.fetchall()
    print(data[1])
    for dict in data:
        if(data):
            print("continue to next page")
            return render_template('AddInfo.html', user=username, flight_info=data)
    return render_template('AddInfo.html', user=username, flight_info=data)
    #Functionality for customer choosing flight
    # if (yes):
    # 	query= 'INSERT into Ticket %s %s %s %s'

#PersonalInformation
@app.route('/personalinfo', methods = ["POST", "GET"])
def bookflight():
    username = session['username']
    if request.method == "POST":
        cursor = conn.cursor()
        form_get = {}
        name = request.form.get('name')
        form_get['Name'] = name
        building_num = request.form.get('building_num')
        form_get['building_num'] = building_num
        street = request.form.get('street')
        form_get['street'] = street
        city = request.form.get('city')
        form_get['City'] = city
        state = request.form.get('State')
        form_get['State'] = state
        passport = request.form.get('passport')
        form_get['passport'] = passport
        query = 'Select Name, building_num, street, City, State, passport from Customer where email = %s'
        cursor.execute(query, username)
        data = cursor.fetchone()
        print('Database', data)
        print('Post_data', form_get)
        if(data == form_get):
            print("Information is correct")
            conn.commit()
            cursor.close()
            return render_template('Payment.html', user=username)
        else:
            error = "Personal information is incorrect. Doesn't match the user records"
            return render_template("PersonalInfo.html", user = username, error=error)
    return render_template("PersonalInfo.html", user=username)

#PAYMENT
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    username = session['username']
    if request.method == "POST":
        cursor = conn.cursor()
        card_type = request.form.get('credit/debit')
        card_num = request.form.get('card_num')
        name_on_card = request.form.get('card_name')
        exp_date = request.form.get('exp_date')
        form_get = {}
        form_get['card_number'] = card_type
        form_get['card_type'] = card_num
        form_get['Name_on_card'] = name_on_card
        form_get['Expiration_date'] = exp_date
        query = 'SELECT card_number, card_type, Name_on_card, Expiration_date FROM Ticket WHERE Email = %s'
        cursor.execute(query, (username))
        data = cursor.fetchone()
        print(data)
        error = None
        if(data == form_get):
            error = 'Payment information already exists'
            return render_template('Payment.html', error=error)
        else:
            new_info = 'INSERT INTO ticket VALUES(%s, %s, %s, %s)'
            cursor.execute(new_info, (card_type, card_num, name_on_card, exp_date))
            conn.commit()
            cursor.close()
            return render_template("Confirm.html", new_info = data, user=username)
    return render_template('Payment.html')
        

#Confirmation page for information
#Update the profile with the information
@app.route('/confirm')
def confirm():
    username = session['username']
    #Extract information from addinfo
    #Arrange it using html
    return render_template('Finalize.html', user=username)


'''
#Future Flights
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



#Authenticates the register
@app.route('/register', methods=['GET', 'POST'])
def register():
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
    cursor = conn.cursor()
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall() 
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('home.html', username=username, posts=data1)


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')


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


#Adds confirmation page
@app.route('/confirm')
def confirm():
    
return render_template('Finalize.html')


#User authentification

'''

if __name__ == "__main__": 
    app.run('127.0.0.1', 5000, debug= True )

