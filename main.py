from flask import Flask, render_template, request, session, url_for, redirect
import bcrypt
import pymysql.cursors
import mysql
import random


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
    
    return redirect(url_for('home', message=message))



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
@app.route('/profile', methods = ['GET', 'POST'])
#Load up any flights where id is the same 
#And display them 
def profile():
    total_spending = 0
    customer = session['customer']
    cursor = conn.cursor()
    #Selects ticket information where username is same and orders it by time
    query = 'SELECT Ticket_id, flight_number, sold_price FROM ticket NATURAL JOIN Customer WHERE Customer.EMAIL = %s AND Customer.EMAIL = ticket.EMAIL'
    cursor.execute(query, (customer))
    data1 = cursor.fetchall()
    cursor.close()
    for dict in data1:
        total_spending += dict['sold_price']
    if request.method == 'POST':
        cursor = conn.cursor()
        flight_id = request.form.get('flight_id')
        name = request.form.get('name')
        rating = request.form.get('rating')
        comments = request.form.get('comments')
        query1 = 'SELECT flight_number from Ticket where flight_number = %s'
        cursor.execute(query1, flight_id )
        data2 = cursor.fetchall()
        result = None
        print(data2)
        if data2:
            result = "Thank you for your review!"
            insert = 'Insert INTO customer_review VALUES(%s, %s, %s, %s)'
            cursor.execute(insert, (flight_id, name, rating, comments))
            conn.commit()
            cursor.close()
            return render_template("MyProfile.html", info=data2, customer=customer, result = result, tot_spend = total_spending)
        else:
            result = "Error. Flight not found"
            return render_template("MyProfile.html", info=data2, customer=customer, result= result, tot_spend = total_spending)

    return render_template("MyProfile.html", info = data1, customer=customer, tot_spend = total_spending)



#STAFF INFO 

#STAFF Profile
@app.route('/staffprofile', methods = ['GET', 'POST'])
def staffprofile():
    username = session['staff'] 
    cursor = conn.cursor()
    #Selects all of airline staff flights
    # query = 'SELECT * FROM FLIGHT NATURAL JOIN AirlineStaff WHERE AirlineStaff.Airline_name = Flight.Airline_name'
    # cursor.execute(query)
    # staff_flights = cursor.fetchall()
    # query = 'SELECT * from customer_review'
    # cursor.execute(query)
    # reviews = cursor.fetchall()
    query = 'SELECT Airline_name FROM airlineStaff WHERE username = %s'
    cursor.execute(query, (username))
    airline = cursor.fetchone()
    query = 'SELECT * FROM flight WHERE airline_name = %s'
    cursor.execute(query, (airline['Airline_name']))
    flights = cursor.fetchall()
    query = 'SELECT Email FROM ticket GROUP BY Email ORDER BY COUNT(*) DESC LIMIT 1'
    cursor.execute(query)
    email = cursor.fetchall()
    query = 'SELECT Name FROM customer WHERE email = %s'
    cursor.execute(query, (email[0]['Email']))
    mostfrequent = cursor.fetchone()
    query = "SELECT SUM(sold_price) AS 'total_year'  FROM ticket WHERE purchase_date > DATE_ADD(NOW(), INTERVAL -1 MONTH) AND Airline_name = %s"
    cursor.execute(query, (airline['Airline_name']))
    total_year = cursor.fetchone()
    totalyear = total_year['total_year']
    query = "SELECT SUM(sold_price) AS 'total_month' FROM ticket WHERE purchase_date > DATE_ADD(NOW(), INTERVAL -1 YEAR) AND Airline_name = %s"
    cursor.execute(query, (airline['Airline_name']))
    total_month = cursor.fetchone()
    totalmonth = total_month['total_month']
    query = "SELECT COUNT(*) AS 'count_year'  FROM ticket WHERE purchase_date > DATE_ADD(NOW(), INTERVAL -1 YEAR) AND Airline_name = %s"
    cursor.execute(query, (airline['Airline_name']))
    count_year = cursor.fetchone()
    query = "SELECT COUNT(*) AS 'count_month' FROM ticket WHERE purchase_date > DATE_ADD(NOW(), INTERVAL -1 MONTH) AND Airline_name = %s"
    cursor.execute(query, (airline['Airline_name']))
    count_month = cursor.fetchone()


    if request.method == 'POST':
        reviews = None
        customerflights = None
        flightid_rating = None
        email = None
        averagerating = None
        flightid_rating = request.form.get('flightid_rating')
        if flightid_rating:
            query = 'SELECT * FROM customer_review WHERE flight_id = %s'
            cursor.execute(query, (flightid_rating))
            reviews = cursor.fetchall()
            print(reviews)
            # get avrage rating for flight
            query = "SELECT AVG(rating) AS 'averagerating' FROM customer_review WHERE flight_id = %s"
            cursor.execute(query, (flightid_rating))
            averagerating = cursor.fetchone()
    
        email = request.form.get('email')
        if email:
            query = 'SELECT * FROM ticket NATURAL JOIN flight WHERE ticket.Email = %s AND flight.Airline_name = %s AND ticket.flight_number = flight.flight_number'
            cursor.execute(query, (email, airline['Airline_name']))
            customerflights = cursor.fetchall()
        
        return render_template("staffprofile.html", staffuser = username, averagerating=averagerating,  reviews=reviews, flights=flights,mostfrequent=mostfrequent,customerflights=customerflights,total_year=total_year,total_month=total_month,count_year=count_year,count_month=count_month)
    else:
        return render_template("staffprofile.html", staffuser = username,flights=flights,mostfrequent=mostfrequent,total_month=total_month,total_year=total_year,count_year=count_year,count_month=count_month)

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

        
@app.route('/addairport', methods=['GET', 'POST'])
def addairport():
    if request.method == "POST":
        airport_name = request.form.get('Name')
        city = request.form.get('city')
        country = request.form.get('country')
        AirportType = request.form.get('AirportType')
        cursor = conn.cursor()
        query = 'SELECT * from airport WHERE Name= %s'
        cursor.execute(query, (airport_name))
        data = cursor.fetchone()
        error = None
        if(data):
            message = "This airport already exists"
            return render_template("addairport.html", message=message)
        else:
            ins = 'INSERT INTO airport VALUES(%s, %s, %s, %s)'
            cursor.execute(ins, (airport_name, city, country, AirportType))
            conn.commit()
            cursor.close()
            message = "Airport added successfully"
            return render_template('addairport.html', message=message)
    else:
        return render_template('addairport.html')

@app.route('/addairplane', methods=['GET', 'POST'])
def addairplane():
    if request.method == "POST":
        airplane_id = request.form.get('airplane_id')
        Name = request.form.get('Name')
        Manufacturing_company = request.form.get('Manufacturing_company')
        Num_of_seats = request.form.get('Num_of_seats')
        Age = request.form.get('Age')
        airline_name = request.form.get('airline_name')
        cursor = conn.cursor()
        query = 'SELECT * from airplane WHERE airplane_id= %s'
        cursor.execute(query, (airplane_id))
        data = cursor.fetchone()
        error = None
        if(data):
            message = "This airplane already exists"
            return render_template("addairplane.html", message=message)
        else:
            ins = 'INSERT INTO airplane VALUES(%s, %s, %s, %s, %s, %s)'
            cursor.execute(ins, (airplane_id, Name, Manufacturing_company, Num_of_seats, Age, airline_name))
            conn.commit()
            cursor.close()
            message = "Airplane added successfully"
            return render_template('addairplane.html', message=message)
    else:
        cursor = conn.cursor()
        query = 'SELECT Airline_name FROM airline'
        cursor.execute(query)
        airlines = cursor.fetchall()
        cursor.execute(query)
        return render_template('addairplane.html', airlines=airlines)

#Adds the flight,airport, and airplane
@app.route('/addflight', methods=['GET', 'POST'])
def addflight():
    if request.method == "POST":
        i = 0
        while i < 1:
            flight_num = random.randint(1000,9999)
            cursor = conn.cursor()
            query = 'SELECT * FROM ticket WHERE Ticket_id = %s'
            cursor.execute(query, (flight_num))
            bool = cursor.fetchone()
            cursor.close()
            # if bool is null, then the id is unique
            if bool == None:
                i += 1
        price = request.form.get('price')
        departure_airport = request.form.get('departure_airport')
        departure_date = request.form.get('departure_date')
        departure_time = request.form.get('departure_time')
        arrival_airport = request.form.get('arrival_airport')
        arrival_date = request.form.get('arrival_date')
        arrival_time = request.form.get('arrival_time')
        airplane_id = request.form.get('airplane_id')
        status = request.form.get('status')
        # airline_name = request.form.get('airline_name')
        airline_name = 'Jet Blue'

        print(airline_name)
        cursor = conn.cursor()
        query = 'SELECT * FROM flight WHERE flight_number = %s'
        cursor.execute(query, (flight_num))
        data = cursor.fetchone()
   
        error = None
        if(data):
            message = "This flight already exists"
            return render_template("addflight.html", message=message)
        else:
            ins = 'INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(ins, (flight_num, price, departure_airport, departure_date, departure_time, arrival_airport, arrival_date, arrival_time, status, airline_name,  airplane_id))
            conn.commit()
            cursor.close()
            message = "Flight added successfully"
            return render_template('addflight.html', message=message)
    else:
        cursor = conn.cursor()
        query = 'SELECT Name FROM airport'
        cursor.execute(query)
        airports = cursor.fetchall()
        query = 'SELECT Airline_name FROM airline'
        cursor.execute(query)
        airlines = cursor.fetchall()
        query = 'SELECT Airplane_id FROM airplane'
        cursor.execute(query)
        airplanes = cursor.fetchall()
        cursor.close()
        print(airlines)
        print(len(airlines))
        return render_template('AddFlight.html',airports=airports, airlines=airlines, airplanes=airplanes)

@app.route('/bookflight/<flight_num>', methods=['GET', 'POST'])
def bookflight(flight_num):
    if request.method == "POST":
        customer = request.form.get('customer')
        cursor = conn.cursor()
        query = 'SELECT Base_price FROM flight WHERE flight_number = %s'
        cursor.execute(query, (flight_num))
        data = cursor.fetchone()
        query = 'SELECT Airline_name FROM flight WHERE flight_number = %s'
        cursor.execute(query, (flight_num))
        airline = cursor.fetchone()
        if(data):
            # redirect to payment page
            email = session['customer']
            price = data.get('Base_price')
            i = 0
            while i < 1:
                ticket_id = random.randint(1000,9999)
                cursor = conn.cursor()
                query = 'SELECT * FROM ticket WHERE Ticket_id = %s'
                cursor.execute(query, (flight_num))
                bool = cursor.fetchone()
                cursor.close()
                # if bool is null, then the id is unique
                if bool == None:
                    i += 1
            card_type = request.form.get('credit/debit')
            card_num = request.form.get('card_num')
            name_on_card = request.form.get('card_name')
            exp_date = request.form.get('exp_date')
            cursor = conn.cursor()
            ins = 'INSERT INTO ticket VALUES(%s, %s, %s, %s, %s, %s, %s, %s, NOW(),%s)'
            print(ticket_id,email,flight_num,price,card_type,card_num,name_on_card,exp_date,airline['Airline_name'])
            cursor.execute(ins, (ticket_id,email,flight_num,price,card_type,card_num,name_on_card,exp_date,airline['Airline_name']))
            conn.commit()
            cursor.close()
            message = "Flight booked successfully"
            return redirect(url_for('home', message=message))
        else:
            message = "This flight does not exist"
            return render_template("bookflight.html", message=message)
    else:
        print(flight_num)
        return render_template('payment.html',flight_num=flight_num)

@app.route('/editflight/<flight_num>', methods=['GET', 'POST'])
def editflight(flight_num):
    if request.method == "POST":
        cursor = conn.cursor()
        query = 'SELECT * FROM flight WHERE flight_number = %s'
        cursor.execute(query, (flight_num))
        data = cursor.fetchone()
        status = request.form.get('status')

        if(data):
            ins = 'UPDATE flight SET flight_status = %s WHERE flight_number = %s'
            cursor.execute(ins, (status, flight_num))
            conn.commit()
            cursor.close()
            message = "Flight updated successfully"
            return render_template('editflight.html', message=message, flights=data,flight_num=flight_num)
        else:
            message = "This flight does not exist"
            return render_template("editflight.html", message=message, flights=data,flight_num=flight_num)
    else:
        cursor = conn.cursor()
        query = 'SELECT * FROM flight WHERE flight_number = %s'
        cursor.execute(query, (flight_num))
        data = cursor.fetchone()
        print(data)
        cursor.close()
        return render_template('editflight.html', flights=data,flight_num=flight_num)

@app.route('/cancelflight', methods = ['GET', 'POST'])
def cancelflight():
    customer = session['customer']
    cursor = conn.cursor()
    query = 'SELECT * FROM Flight NATURAL JOIN Ticket WHERE Flight.flight_number = Ticket.flight_number and Ticket.Email = %s' 
    cursor.execute(query, (customer))
    flight_info = cursor.fetchall()
    cursor.close()
    #Remove information 
    if request.method == "POST":
        ticket = request.form.get('ticket_id')
        print(ticket)
        cursor = conn.cursor()
        query2 = 'DELETE FROM Ticket WHERE Ticket_id = %s' 
        cursor.execute(query2, (ticket))
        conn.commit()
        cursor.close()
        confirmation = "Successfully cancelled flight"
        return render_template('CancelFlight.html', flights = flight_info, user = customer, confirm = confirmation)
    return render_template('CancelFlight.html', flights = flight_info,user = customer)



@app.route('/addinfo', methods= ['GET', 'POST'])
def addinfo():
    if request.method == "POST":
        cursor = conn.cursor()
        query = 'SELECT Name from airport'
        cursor.execute(query)
        airports = cursor.fetchall()
        cursor.close()
        customer = session['customer']
        departure_airport = request.form.get('departure_airport')
        departure_date = request.form.get('departure_date')
        arrival_airport = request.form.get('arrival_airport')
        return_date = request.form.get('return_date')
        bool1 = True
        bool2 = True
        if return_date == None:
            cursor = conn.cursor()
            query = 'SELECT * FROM flight WHERE departure_airport = %s AND departure_date = %s AND arrival_airport = %s'
            cursor.execute(query, (departure_airport, departure_date, arrival_airport))
            data = cursor.fetchall()
            cursor.close()
            print(departure_airport, departure_date, arrival_airport)
            print(data)
            return render_template("Addinfo.html", user=customer, flights=data, bool1=bool1, airports=airports)
        else:
            cursor = conn.cursor()
            query = 'SELECT * FROM flight WHERE departure_airport = %s AND departure_date = %s AND arrival_airport = %s'
            cursor.execute(query, (departure_airport, departure_date, arrival_airport))
            data1 = cursor.fetchall()
            query = 'SELECT * FROM flight WHERE departure_airport = %s AND departure_date = %s AND arrival_airport = %s'
            cursor.execute(query, (arrival_airport, return_date, departure_airport))
            data2 = cursor.fetchall()
            cursor.close()
            print(departure_airport, departure_date, arrival_airport)
            return_date = None
            return render_template("Addinfo.html", user=customer, departure_flight=data1, return_flight=data2, bool2=bool2, airports=airports)
    else:
        cursor = conn.cursor()
        query = 'SELECT Name from airport'
        cursor.execute(query)
        airports = cursor.fetchall()
        cursor.close()
        if 'customer' in session:
            customer = session['customer']
            return render_template("Addinfo.html", user=customer, airports=airports)
        else:
            return render_template("Addinfo.html", airports=airports)

#DO NOW
# #Adds on to previous function based on query
# @app.route('/bookflight', methods = ['GET', 'POST'])
# def addmoreinfo():
#     username = session['username']
#     cursor = conn.cursor()
#     Airline = request.form.get('Airline')
#     departure_airport = request.form.get('departure_airport')
#     arrival_date = request.form.get('arrival_date')
#     arrival_airport = request.form.get('arrival_airport')
#     #Create python function that saves all this data and then utilized in confirm function
#     #When generating the ticket 
#     return render_template('PersonalInfo.html', user=username, data)


#PersonalInformation
# @app.route('/personalinfo', methods = ["POST", "GET"])
# def bookflight():
#     username = session['username']
#     if request.method == "POST":
#         cursor = conn.cursor()
#         form_get = {}
#         name = request.form.get('name')
#         form_get['Name'] = name
#         building_num = request.form.get('building_num')
#         form_get['building_num'] = building_num
#         street = request.form.get('street')
#         form_get['street'] = street
#         city = request.form.get('city')
#         form_get['City'] = city
#         state = request.form.get('State')
#         form_get['State'] = state
#         passport = request.form.get('passport')
#         form_get['passport'] = passport
#         query = 'Select Name, building_num, street, City, State, passport from Customer where email = %s'
#         cursor.execute(query, username)
#         data = cursor.fetchone()
#         print('Database', data)
#         print('Post_data', form_get)
#         if(data == form_get):
#             print("Information is correct")
#             conn.commit()
#             cursor.close()
#             return render_template('Payment.html', user=username)
#         else:
#             error = "Personal information is incorrect. Doesn't match the user records"
#             return render_template("PersonalInfo.html", user = username, error=error)
#     return render_template("PersonalInfo.html", user=username)

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
    return render_template('Payment.html',flight_num=flight_num)
        

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

