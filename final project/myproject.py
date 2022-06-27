#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import random

#Initialize the app from Flask
app = Flask(__name__)

conn = pymysql.connect(host='localhost',
                        user='root',
                        password='',
                        db='airlineticketsystem',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)

# conn = pymysql.connect(host='127.0.0.1',
#                        user='root',
#                        password='',
#                        db='airlineticketsystem',
#                        charset='utf8mb4',
# 					   port = 3308,
#                        cursorclass=pymysql.cursors.DictCursor)


#Define a route to hello function

@app.route('/')
def index():
	return render_template('index.html')

#Define route for login
@app.route('/customer_login')
def Clogin():
	return render_template('customer_login.html')

@app.route('/booking_agent_login')
def BAlogin():
	return render_template('booking_agent_login.html')

@app.route('/airline_staff_login')
def ASlogin():
	return render_template('airline_staff_login.html')

#Define route for register
@app.route('/customer_register')
def Cregister():
	return render_template('customer_register.html')

@app.route('/booking_agent_register')
def BAregister():
	return render_template('booking_agent_register.html')

@app.route('/airline_staff_register')
def ASregister():
	return render_template('airline_staff_register.html')

@app.route('/publicsearch_city')
def PsearchC():
	return render_template('publicsearch_city.html')

@app.route('/publicsearch_city_result', methods=['GET', 'POST'])
def PsearchCR():
	departureCity = request.form["departureCity"]
	arrivalCity = request.form["arrivalCity"]
	departureAirport = request.form["departureAirport"]
	arrivalAirport = request.form["arrivalAirport"]
	cursor = conn.cursor()
	query1 = 'SELECT airline_name,flight_num, depart_time, arrive_time, airplane_id, arrive_airport_name,' \
			 ' depart_airport_name, status, price FROM flight, Airport as S, Airport as T WHERE ' \
			'arrive_airport_name = S.airport_name AND S.city = %s AND depart_airport_name = T.airport_name AND ' \
			 'T.city = %s'
	query2 = 'SELECT airline_name,flight_num, depart_time, arrive_time, airplane_id, arrive_airport_name,' \
			 'depart_airport_name, status, price FROM flight WHERE arrive_airport_name = %s AND depart_airport_name = %s'
	if departureAirport == "Any" or arrivalAirport == "Any":
		cursor.execute(query1, (arrivalCity, departureCity))
	else:
		cursor.execute(query2, (arrivalAirport, departureAirport))
	# stores the results in a variable
	data1 = cursor.fetchall()
	for each in data1:
		print(each['airline_name'], each['flight_num'], each['depart_time'], each['arrive_time'], each['airplane_id'],
			  each['arrive_airport_name'], each['depart_airport_name'], each['status'], each['price'])
	cursor.close()
	return render_template('publicsearch_city.html', posts=data1)

@app.route('/publicsearch_flight')
def PsearchF():
	return render_template('publicsearch_flight.html')

@app.route('/publicsearch_flight_result', methods=['GET', 'POST'])
def PsearchFR():
	flight_number = request.form["flight_number"]
	arrival_date = request.form["arrival_date"]
	departure_date = request.form["departure_date"]
	cursor = conn.cursor()
	query1 = 'SELECT status FROM flight WHERE flight_num = %s AND DATE(depart_time) = %s'
	query2 = 'SELECT status FROM flight WHERE flight_num = %s AND DATE(arrive_time) = %s'
	query3 = 'SELECT status FROM flight WHERE flight_num = %s AND DATE(depart_time) = %s AND DATE(arrive_time) = %s'
	if arrival_date == "Any":
		cursor.execute(query1, (flight_number, departure_date))
	elif departure_date == "Any":
		cursor.execute(query2, (flight_number, arrival_date))
	else:
		cursor.execute(query3, (flight_number, departure_date, arrival_date))
	data1 = cursor.fetchall()
	for each in data1:
		print(each['status'])
	cursor.close()
	return render_template('publicsearch_flight.html', posts=data1)
#---------------------------------Authenticates the login----------------------------------------
@app.route('/CloginAuth', methods=['GET', 'POST'])
def CloginAuth():
	#grabs information from the forms
	username = request.form['C_Email']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE customer_email = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['C_Email'] = username
		return redirect(url_for('customer_home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('customer_login.html', error=error)

@app.route('/BAloginAuth', methods=['GET', 'POST'])
def BAloginAuth():
	#grabs information from the forms
	username = request.form['BA_Email']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM booking_agent WHERE agent_email = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['BA_Email'] = username
		return redirect(url_for('booking_agent_home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('booking_agent_login.html', error=error)

@app.route('/ASloginAuth', methods=['GET', 'POST'])
def ASloginAuth():
	#grabs information from the forms
	username = request.form['AS_Username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM airline_staff WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['AS_Username'] = username
		return redirect(url_for('airline_staff_home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('airline_staff_login.html', error=error)



#-----------------------------------Authenticates the register----------------------------------
@app.route('/CregisterAuth', methods=['GET', 'POST'])
def CregisterAuth():
	#grabs information from the forms
	customer_email = request.form['customer_email']
	name = request.form['name']
	password = request.form['password']
	building_num = request.form['building_num']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	phone_number = request.form['phone_number']
	passport_number = request.form['passport_number']
	passport_expiration = request.form['passport_expiration']
	passport_country = request.form['passport_country']
	birth_of_date = request.form['birth_of_date']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE customer_email = %s'
	cursor.execute(query, (customer_email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('customer_register.html', error = error)
	else:
		ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (customer_email, name, password, building_num, street, city, state, phone_number, passport_number, passport_expiration, passport_country, birth_of_date))
		conn.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/BAregisterAuth', methods=['GET', 'POST'])
def BAregisterAuth():
	#grabs information from the forms
	username = request.form['BAusername']
	password = request.form['password']
	booking_agent_id = request.form['booking_agent_id']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM booking_agent WHERE agent_email = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('booking_agent_register.html', error = error)
	else:
		ins = 'INSERT INTO booking_agent VALUES(%s, %s, %s)'
		cursor.execute(ins, (username, password, booking_agent_id))
		conn.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/ASregisterAuth', methods=['GET', 'POST'])
def ASregisterAuth():
	#grabs information from the forms
	AS_Username = request.form['AS_Username']
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	date_of_birth = request.form['date_of_birth']
	airline_name = request.form['airline_name']
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM airline_staff WHERE username = %s'
	cursor.execute(query, (AS_Username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('airline_staff_register.html', error = error)
	else:
		ins = 'INSERT INTO airline_staff VALUES(%s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (AS_Username, password, first_name, last_name, date_of_birth, airline_name))
		conn.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/customer_home')
def customer_home():
	return render_template('customer_home.html')

@app.route('/booking_agent_home')
def booking_agent_home():
	return render_template('booking_agent_home.html')

@app.route('/airline_staff_home')
def airline_staff_home():
	return render_template('airline_staff_home.html')
# ---------------------------------customer ------------------------------------------

@app.route('/customer_view_my_flights', methods=["GET", "POST"])
def customer_view_my_flights():
	if session.get("C_Email"):
		customer_email = session["C_Email"]

	cursor = conn.cursor()
	query = 'SELECT * FROM flight, ticket, purchase' \
			' where customer_email = %s' \
			' and purchase.ticket_id = ticket.ticket_id and ticket.flight_num = flight.flight_num and flight.airline_name = ticket.airline_name'
	cursor.execute(query, (customer_email))
	# stores the results in a variable
	data = cursor.fetchall()
	for each in data:
		print(each['airline_name'], each['flight_num'], each['depart_time'], each['arrive_time'], each['airplane_id'],
			  each['arrive_airport_name'], each['depart_airport_name'], each['status'], each['price'])
	cursor.close()

	return render_template('customer_view_my_flights.html', data=data)


@app.route('/customer_purchase_tickets')
def customer_purchase_tickets():
	return render_template('/customer_purchase_tickets.html')

@app.route('/customer_purchase_tickets_result', methods=["GET", "POST"])
def customer_purchase_tickets_result():
	if session.get("C_Email"):
		customer_email = session["C_Email"]

	flight_num = request.form['flight_num']
	airline_name = request.form['airline_name']

	cursor = conn.cursor()
	ticket_id = str(random.randint(0, 999))
	query1 = "insert into ticket values (%s, %s, %s)"
	query2 = 'insert into purchase values (%s, null, %s, now())'
	cursor.execute(query1, (ticket_id, flight_num, airline_name))
	cursor.execute(query2, (ticket_id, customer_email))
	conn.commit()
	cursor.close()
	return render_template('customer_home.html')


@app.route('/customer_search_flights')
def customer_search_flights():
	return render_template('customer_search_flights.html')


@app.route('/customer_search_flights_result', methods=["GET", "POST"])
def customer_search_flights_result():
	if session.get("C_Email"):
		customer_email = session["C_Email"]

	departureCity = request.form["departureCity"]
	arrivalCity = request.form["arrivalCity"]
	departureAirport = request.form["departureAirport"]
	arrivalAirport = request.form["arrivalAirport"]
	arrivalDate = request.form["arrivalDate"]

	cursor = conn.cursor()
	query1 = 'SELECT airline_name,flight_num, depart_time, arrive_time, airplane_id, arrive_airport_name,' \
	' depart_airport_name, status, price FROM flight, Airport as S, Airport as T WHERE ' \
	'arrive_airport_name = S.airport_name AND S.city = %s AND depart_airport_name = T.airport_name AND ' \
	'T.city = %s AND status = "upcoming" AND DATE(arrive_time) = %s'
	query2 = 'SELECT airline_name,flight_num, depart_time, arrive_time, airplane_id, arrive_airport_name,' \
			 'depart_airport_name, status, price FROM flight WHERE ' \
			 'arrive_airport_name = %s AND depart_airport_name = %s AND status = "upcoming" AND DATE(arrive_time) = %s'
	if departureAirport == "Any" or arrivalAirport == "Any":
		cursor.execute(query1, (arrivalCity, departureCity, arrivalDate))
	else:
		cursor.execute(query2, (arrivalAirport, departureAirport, arrivalDate))

	data = cursor.fetchall()
	for each in data:
		print(each['airline_name'], each['flight_num'], each['depart_time'], each['arrive_time'], each['airplane_id'],
			  each['arrive_airport_name'], each['depart_airport_name'], each['status'], each['price'])
	cursor.close()
	return render_template('customer_search_flights.html', posts=data)


@app.route('/customer_track_my_spending')
def customer_track_my_spending():
	if session.get("C_Email"):
		customer_email = session["C_Email"]

	cursor = conn.cursor()
	query = 'select price from customer, purchase, ticket, flight ' \
			'where customer.customer_email = %s and customer.customer_email =  purchase.customer_email ' \
			'and purchase.ticket_id = ticket.ticket_id and ticket.flight_num = flight.flight_num'
	cursor.execute(query, (customer_email))
	# stores the results in a variable
	data = cursor.fetchall()
	cursor.close()
	return render_template('customer_track_my_spending.html', data=data)


# -----------------------------------booking agent---------------------------

@app.route('/booking_agent_view_my_flights')
def booking_agent_view_my_flights():
	if session.get("BA_Email"):
		BA_Email = session["BA_Email"]

	cursor = conn.cursor()
	query = 'select * from flight, ticket, purchase, booking_agent ' \
			'where booking_agent.agent_email = %s and booking_agent.agent_email = purchase.agent_email ' \
			'and purchase.ticket_id = ticket.ticket_id and ticket.flight_num = flight.flight_num and ' \
			'flight.airline_name = ticket.airline_name and status = "upcoming"'
	cursor.execute(query, (BA_Email))
	# stores the results in a variable
	data = cursor.fetchall()
	for each in data:
		print(each['customer_email'], each['airline_name'], each['flight_num'], each['depart_time'],
			  each['arrive_time'], each['airplane_id'],
			  each['arrive_airport_name'], each['depart_airport_name'], each['status'], each['price'])
	cursor.close()

	return render_template('booking_agent_view_my_flights.html', data=data)


@app.route('/booking_agent_purchase_tickets', methods=["GET", "POST"])
def booking_agent_purchase_tickets():
	return render_template('booking_agent_purchase_tickets.html')


@app.route('/booking_agent_purchase_tickets_result', methods=["GET", "POST"])
def booking_agent_purchase_tickets_result():
	if session.get("BA_Email"):
		BA_Email = session["BA_Email"]

	customer_email = request.form['customer_email']
	flight_num = request.form['flight_num']
	airline_name = request.form['airline_name']

	cursor = conn.cursor()
	ticket_id = str(random.randint(0, 999))
	query1 = "insert into ticket values (%s, %s, %s)"
	query2 = 'insert into purchase values (%s, %s, %s, now())'
	cursor.execute(query1, (ticket_id, flight_num, airline_name))
	cursor.execute(query2, (ticket_id, BA_Email, customer_email))
	conn.commit()

	cursor.close()

	return render_template('booking_agent_purchase_tickets.html')


@app.route('/booking_agent_search_flights')
def booking_agent_search_flights():
	return render_template('booking_agent_search_flights.html')


@app.route('/booking_agent_search_flights_result', methods=["GET", "POST"])
def booking_agent_search_flights_result():
	if session.get("BA_Email"):
		BA_Email = session["BA_Email"]

	departureCity = request.form["departureCity"]
	arrivalCity = request.form["arrivalCity"]
	departureAirport = request.form["departureAirport"]
	arrivalAirport = request.form["arrivalAirport"]
	arrivalDate = request.form["arrivalDate"]

	cursor = conn.cursor()
	query1 = 'SELECT airline_name,flight_num, depart_time, arrive_time, airplane_id, arrive_airport_name,' \
			 ' depart_airport_name, status, price FROM flight, Airport as S, Airport as T WHERE ' \
			 'arrive_airport_name = S.airport_name AND S.city = %s AND depart_airport_name = T.airport_name AND ' \
			 'T.city = %s AND status = "upcoming" AND DATE(arrive_time) = %s'
	query2 = 'SELECT airline_name,flight_num, depart_time, arrive_time, airplane_id, arrive_airport_name,' \
			 'depart_airport_name, status, price FROM flight WHERE ' \
			 'arrive_airport_name = %s AND depart_airport_name = %s AND status = "upcoming" AND DATE(arrive_time) = %s'
	if departureAirport == "Any" or arrivalAirport == "Any":
		cursor.execute(query1, (arrivalCity, departureCity, arrivalDate))
	else:
		cursor.execute(query2, (arrivalAirport, departureAirport, arrivalDate))

	data = cursor.fetchall()
	for each in data:
		print(each['customer_email'], each['airline_name'], each['flight_num'], each['depart_time'],
			  each['arrive_time'], each['airplane_id'],
			  each['arrive_airport_name'], each['depart_airport_name'], each['status'], each['price'])
	cursor.close()

	return render_template('booking_agent_search_flights.html', posts=data)


@app.route('/booking_agent_view_my_commission', methods=["GET", "POST"])
def booking_agent_view_my_commission():
	if session.get("BA_Email"):
		BA_Email = session["BA_Email"]

	cursor = conn.cursor()
	query = 'select sum(price * 0.1) as total_commission, avg(price * 0.1) as average_commission, count(ticket.ticket_id) as number_of_ticket_sold ' \
			'from purchase, flight, ticket where agent_email = %s and purchase.ticket_id = ticket.ticket_id and ticket.flight_num = flight.flight_num'

	cursor.execute(query, (BA_Email))
	# stores the results in a variable
	data = cursor.fetchall()
	for each in data:
		print(each['total_commission'], each['average_commission'], each['number_of_ticket_sold'])
	cursor.close()
	return render_template('booking_agent_view_my_commission.html', data=data)


@app.route('/booking_agent_view_top_customers')
def booking_agent_view_top_customers():
	return render_template('booking_agent_view_top_customers.html')


@app.route('/booking_agent_view_top_customer_order', methods=["GET", "POST"])
def booking_agent_view_top_customer_order():
	cursor = conn.cursor()
	query = 'select customer.customer_email ' \
			'from customer, purchase, ticket ' \
			'where customer.customer_email =  purchase.customer_email and purchase.ticket_id = ticket.ticket_id and purchase.agent_email is not NULL ' \
			'and purchase_date > date_sub(date(now()), interval 183 day) group by customer.customer_email order by count(ticket.ticket_id) desc ' \
			'limit 5'
	cursor.execute(query)
	# stores the results in a variable
	data = cursor.fetchall()
	for each in data:
		print(each['customer_email'])
	cursor.close()
	return render_template('booking_agent_view_top_customer_order.html', data=data)


@app.route('/booking_agent_view_top_customer_money', methods=["GET", "POST"])
def booking_agent_view_top_customer_money():
	cursor = conn.cursor()
	query = 'select customer.customer_email ' \
			'from customer, purchase, ticket, flight ' \
			'where customer.customer_email =  purchase.customer_email and purchase.ticket_id = ticket.ticket_id and purchase.agent_email ' \
			'is not NULL and ticket.flight_num = flight.flight_num and purchase_date > date_sub(date(now()), interval 365 day) ' \
			'group by customer.customer_email order by sum(flight.price) desc limit 5'
	cursor.execute(query)
	# stores the results in a variable
	data = cursor.fetchall()
	for each in data:
		print(each['customer_email'])
	cursor.close()
	return render_template('booking_agent_view_top_customer_money.html', data=data)


# ----------------------------airline staff-------------------------

@app.route('/airline_staff_view_my_flights')
def airline_staff_view_my_flights():
	username = session['AS_Username']
	return render_template('airline_staff_view_my_flights.html')

@app.route('/airline_staff_view_my_flights_defualt', methods=['GET', 'POST'])
def airline_staff_view_my_flights_default():
	username = session['AS_Username']
	cursor = conn.cursor()
	start_date = request.form["start_date"]
	end_date = request.form["end_date"]
	departureCity = request.form["departureCity"]
	arrivalCity = request.form["arrivalCity"]
	departureAirport = request.form["departureAirport"]
	arrivalAirport = request.form["arrivalAirport"]
	query_d = 'select * from flight, airline_staff where airline_staff.username = %s and airline_staff.airline_name = ' \
			'flight.airline_name and depart_time < (date_add(now(), interval 30 day))'

	query1 = 'SELECT * FROM flight, Airline_Staff, Airport as S, Airport as T WHERE Airline_Staff.username = %s' \
			 ' and Airline_Staff.airline_name = flight.airline_name AND DATE(depart_time) >= %s AND ' \
			 'DATE(depart_time) <= %s AND arrive_airport_name = S.airport_name AND arrive_airport_name = %s ' \
			 'AND S.city = %s AND depart_airport_name = T.airport_name AND depart_airport_name = %s AND T.city = %s'
	if start_date == "D" or end_date == "D" or departureCity == "D" or arrivalCity == "D" or departureAirport == "D" \
			or arrivalAirport == "D":
		cursor.execute(query_d, username)
	else:
		cursor.execute(query1, (username, start_date, end_date, arrivalAirport, arrivalCity, departureAirport, departureCity))
	data1 = cursor.fetchall()
	for each in data1:
		print(each['airline_name'], each['flight_num'], each['depart_time'], each['arrive_time'], each['airplane_id'],
			  each['arrive_airport_name'], each['depart_airport_name'], each['status'], each['price'])
	conn.commit()
	cursor.close()
	return render_template('airline_staff_view_my_flights.html', username=username, posts=data1)

@app.route('/airline_staff_view_my_flights_find_c', methods=['GET', 'POST'])
def airline_staff_view_my_flights_find_c():
	username = session['AS_Username']
	cursor = conn.cursor()
	flight_num = request.form["flight_num"]
	airline_name = request.form["airline_name"]
	query2 = 'select customer.customer_email, customer_name from customer, purchase, ticket, flight where ' \
				 'flight.flight_num = %s and flight.airline_name = %s and customer.customer_email = ' \
				 'purchase.customer_email and purchase.ticket_id = ticket.ticket_id and ticket.flight_num = ' \
				 'flight.flight_num and flight.airline_name = ticket.airline_name'
	cursor.execute(query2, (flight_num, airline_name))
	data1 = cursor.fetchall()
	for each in data1:
		print(each['customer_name'], each['customer_email'])
	conn.commit()
	cursor.close()
	return render_template('airline_staff_view_my_flights.html', username=username, posts=data1)

@app.route('/airline_staff_create_flights')
def airline_staff_create_flights():
	username = session['AS_Username']
	cursor = conn.cursor()
	query = 'select * from flight, airline_staff where airline_staff.username = %s and airline_staff.airline_name = ' \
			'flight.airline_name and depart_time < (date_add(now(), interval 30 day))'
	cursor.execute(query, (username))
	data1 = cursor.fetchall()
	for each in data1:
		print(each['airline_name'], each['flight_num'], each['depart_time'], each['arrive_time'], each['airplane_id'],
			  each['arrive_airport_name'], each['depart_airport_name'], each['status'], each['price'])
	conn.commit()
	cursor.close()
	return render_template('airline_staff_create_flights.html', posts = data1)

@app.route('/create_flights', methods=['GET', 'POST'])
def create_flights():
	username = session['AS_Username']
	flight_num = request.form['flight_num']
	airline_name = request.form['airline_name']
	depart_time = request.form['depart_time']
	arrive_time = request.form['arrive_time']
	price = request.form['price']
	status = request.form['status']
	airplane_id = request.form['airplane_id']
	depart_airport_name = request.form['depart_airport_name']
	arrive_airport_name = request.form['arrive_airport_name']
	cursor = conn.cursor()
	query = 'INSERT INTO flight (airline_name,flight_num, depart_time, arrive_time, airplane_id, arrive_airport_name,' \
			 ' depart_airport_name, status, price) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
	cursor.execute(query, (airline_name,flight_num, depart_time, arrive_time, airplane_id, arrive_airport_name,
						   depart_airport_name, status, price))
	conn.commit()
	cursor.close()
	return redirect(url_for('airline_staff_home'))

@app.route('/airline_staff_change_flight_status')
def airline_staff_change_flight_status():
	username = session['AS_Username']
	return render_template('airline_staff_change_flight_status.html')

@app.route('/change_flights', methods=['GET', 'POST'])
def update_flights():
	username = session['AS_Username']
	flight_num = request.form['flight_num']
	airline_name = request.form['airline_name']
	status = request.form['status']
	cursor = conn.cursor()
	query = 'UPDATE Flight SET status = %s WHERE (flight_num, airline_name) = (%s, %s)'
	cursor.execute(query, (status, flight_num, airline_name))
	conn.commit()
	cursor.close()
	return redirect(url_for('airline_staff_home'))

@app.route('/airline_staff_add_airplane')
def airline_staff_add_airplane():
	username = session['AS_Username']
	cursor = conn.cursor()
	query = 'select airplane_id, airline.airline_name, seats from (airline join airplane using (airline_name)), ' \
			'airline_staff where airline_staff.airline_name = airline.airline_name and username = %s'
	cursor.execute(query, (username))
	data1 = cursor.fetchall()
	for each in data1:
		print(each['airplane_id'], each['airline_name'], each['seats'])
	conn.commit()
	cursor.close()
	return render_template('airline_staff_add_airplane.html', posts=data1, username=username)

@app.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
	username = session['AS_Username']
	airplane_id = request.form['airplane_id']
	airline_name = request.form['airline_name']
	seats = request.form['seats']
	cursor = conn.cursor()
	query = 'INSERT INTO airplane (airplane_id, airline_name, seats) VALUES(%s, %s, %s)'
	cursor.execute(query, (airplane_id, airline_name, seats))
	conn.commit()
	cursor.close()
	return redirect(url_for('airline_staff_home'))

@app.route('/airline_staff_add_airport')
def airline_staff_add_airport():
	username = session['AS_Username']
	return render_template('airline_staff_add_airport.html')

@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
	username = session['AS_Username']
	airport_name = request.form['airport_name']
	city = request.form['city']
	cursor = conn.cursor()
	query = 'INSERT INTO airport (airport_name, city) VALUES(%s, %s)'
	cursor.execute(query, (airport_name, city))
	conn.commit()
	cursor.close()
	return redirect(url_for('airline_staff_home'))

@app.route('/airline_staff_view_booking_agents')
def airline_staff_view_booking_agents():
	username = session['AS_Username']
	cursor = conn.cursor()
	query_num_month = 'select booking_agent.agent_email, count(ticket_id) from booking_agent, purchase where ' \
			'booking_agent.agent_email = purchase.agent_email and purchase_date > date_sub(date(now()), interval 30 day) ' \
			'group by booking_agent.agent_email' \
			' order by count(ticket_id) limit 5'
	query_num_year = 'select booking_agent.agent_email, count(ticket_id) from booking_agent, purchase where ' \
					 'booking_agent.agent_email = purchase. agent_email and purchase_date > date_sub(date(now()), ' \
					 'interval 365 day) group by booking_agent.agent_email order by count(ticket_id) limit 5'
	query_commission = 'select booking_agent.agent_email, sum(price * 0.1) as tot_commision from purchase, ' \
					   'booking_agent, flight, ticket where booking_agent.agent_email = purchase. agent_email and ' \
					   'purchase_date > date_sub(date(now()), interval 365 day) and purchase.ticket_id = ' \
					   'ticket.ticket_id and ticket.flight_num = flight.flight_num group by booking_agent.agent_email'
	cursor.execute(query_num_month)
	data2 = cursor.fetchall()
	cursor.execute(query_num_year)
	data3 = cursor.fetchall()
	cursor.execute(query_commission)
	data1 = cursor.fetchall()
	for each in data1:
		print(each['agent_email'])
	for each in data2:
		print(each['agent_email'])
	for each in data3:
		print(each['agent_email'])
	conn.commit()
	cursor.close()
	return render_template('airline_staff_view_booking_agents.html', posts1 = data1, posts2 = data2, posts3 = data3)

@app.route('/airline_staff_view_frequent_customers', methods=['GET', 'POST'])
def airline_staff_view_frequent_customers():
	username = session['AS_Username']
	cursor = conn.cursor()
	query = 'select customer_email, count(ticket_id) from purchase where purchase_date > date_sub(date(now()),interval ' \
			'365 day) group by customer_email desc order by count(ticket_id) LIMIT 1'
	cursor.execute(query)
	data1 = cursor.fetchall()
	for each in data1:
	 	print(each['customer_email'])
	conn.commit()
	cursor.close()
	return render_template('airline_staff_view_frequent_customers.html', posts1 = data1)

@app.route('/customer_flights', methods=['GET', 'POST'])
def customer_flights():
	username = session['AS_Username']
	customer_email = request.form['customer_email']
	cursor = conn.cursor()
	query = 'select flight_num, airline_name from purchase join ticket using (ticket_id) where ' \
			'purchase.customer_email = %s'
	cursor.execute(query, customer_email)
	data2 = cursor.fetchall()
	for each in data2:
		print(each['flight_num'], each['airline_name'])
	query = 'select customer_email, count(ticket_id) from purchase where purchase_date > date_sub(date(now()),interval ' \
			'365 day) group by customer_email desc order by count(ticket_id) LIMIT 1'
	cursor.execute(query)
	data1 = cursor.fetchall()
	for each in data1:
		print(each['customer_email'])
	conn.commit()
	cursor.close()
	return render_template('airline_staff_view_frequent_customers.html', posts1 = data1, posts2=data2)

@app.route('/airline_staff_view_reports')
def airline_staff_view_reports():
	username = session['AS_Username']
	return render_template('airline_staff_view_reports.html')

@app.route('/airline_staff_comparison_of_revenue_earned')
def airline_staff_comparison_of_revenue_earned():
	username = session['AS_Username']
	return render_template('airline_staff_comparison_of_revenue_earned.html')

@app.route('/airline_staff_view_top_destinations', methods=['GET', 'POST'])
def airline_staff_view_top_destinations():
	username = session['AS_Username']
	cursor = conn.cursor()
	query_month = 'SELECT COUNT(t.Ticket_ID) total_ticket_num, city FROM Ticket t, purchase p, Flight f, Airport c ' \
				  'WHERE t.airline_name = (SELECT airline_name FROM airline_staff WHERE username = %s) AND' \
				  ' t.Ticket_ID = p.Ticket_ID AND p.purchase_date >= DATE_SUB(NOW(),INTERVAL 90 DAY) AND ' \
				  'p.purchase_date <= NOW() AND (t.airline_name, t.flight_num) = (f.airline_name, f.flight_num) AND ' \
				  'f.arrive_airport_name = c.airport_name GROUP BY c.city LIMIT 3'
	query_year = 'SELECT COUNT(t.Ticket_ID) total_ticket_num, city FROM Ticket t, purchase p, Flight f, Airport c ' \
				  'WHERE t.airline_name = (SELECT airline_name FROM airline_staff WHERE username = %s) AND' \
				  ' t.Ticket_ID = p.Ticket_ID AND p.purchase_date >= DATE_SUB(NOW(),INTERVAL 365 DAY) AND ' \
				  'p.purchase_date <= NOW() AND (t.airline_name, t.flight_num) = (f.airline_name, f.flight_num) AND ' \
				  'f.arrive_airport_name = c.airport_name GROUP BY c.city LIMIT 3'
	cursor.execute(query_month)
	data1 = cursor.fetchall()
	cursor.execute(query_year)
	data2 = cursor.fetchall()
	for each in data1:
		print(each['city'])
	for each in data2:
		print(each['city'])
	conn.commit()
	cursor.close()
	return render_template('airline_staff_view_top_destinations.html', posts1 = data1, posts2=data2)

@app.route('/C_logout')
def C_logout():
	session.pop('C_Email')
	return redirect('/')

@app.route('/BA_logout')
def BA_logout():
	session.pop('BA_Email')
	return redirect('/')

@app.route('/AS_logout')
def AS_logout():
	session.pop('AS_Username')
	return redirect('/')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)