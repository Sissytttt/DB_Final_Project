#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

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

@app.route('/publicsearch_location')
def PsearchL():
	return render_template('publicsearch_location.html')

@app.route('/publicsearch_flight')
def PsearchF():
	return render_template('publicsearch_flight.html')

#---------------------------------Authenticates the login----------------------------------------
@app.route('/CloginAuth', methods=['GET', 'POST'])
def CloginAuth():
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
		session['username'] = username
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
		return redirect(url_for('airline_staff_home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('airline_staff_login.html', error=error)



#-----------------------------------Authenticates the register----------------------------------
@app.route('/CregisterAuth', methods=['GET', 'POST'])
def CregisterAuth():
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
		return render_template('customer_register.html', error = error)
	else:
		ins = 'INSERT INTO user VALUES(%s, %s)'
		cursor.execute(ins, (username, password))
		conn.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/BAregisterAuth', methods=['GET', 'POST'])
def BAregisterAuth():
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
		return render_template('booking_agent_register.html', error = error)
	else:
		ins = 'INSERT INTO user VALUES(%s, %s)'
		cursor.execute(ins, (username, password))
		conn.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/ASregisterAuth', methods=['GET', 'POST'])
def ASregisterAuth():
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
		return render_template('airline_staff_register.html', error = error)
	else:
		ins = 'INSERT INTO user VALUES(%s, %s)'
		cursor.execute(ins, (username, password))
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

@app.route('/customer_view_my_flights')
def customer_view_my_flights():
	return render_template('customer_view_my_flights.html')

@app.route('/customer_purchase_tickets')
def customer_purchase_tickets():
	return render_template('customer_purchase_tickets.html')

@app.route('/customer_search_flights')
def customer_search_flights():
	return render_template('customer_search_flights.html')

@app.route('/customer_track_my_spending')
def customer_track_my_spending():
	return render_template('customer_track_my_spending.html')

@app.route('/booking_agent_view_my_flights')
def booking_agent_view_my_flights():
	return render_template('booking_agent_view_my_flights.html')

@app.route('/booking_agent_purchase_tickets')
def booking_agent_purchase_tickets():
	return render_template('booking_agent_purchase_tickets.html')

@app.route('/booking_agent_search_flights')
def booking_agent_search_flights():
	return render_template('booking_agent_search_flights.html')

@app.route('/booking_agent_view_my_commission')
def booking_agent_view_my_commission():
	return render_template('booking_agent_view_my_commission.html')

@app.route('/booking_agent_view_top_customers')
def booking_agent_view_top_customers():
	return render_template('booking_agent_view_top_customers.html')

@app.route('/airline_staff_view_my_flights')
def airline_staff_view_my_flights():
	return render_template('airline_staff_view_my_flights.html')

@app.route('/airline_staff_create_flights')
def airline_staff_create_flights():
	return render_template('airline_staff_create_flights.html')

@app.route('/airline_staff_change_flight_status')
def airline_staff_change_flight_status():
	return render_template('airline_staff_change_flight_status.html')

@app.route('/airline_staff_add_airplane')
def airline_staff_add_airplane():
	return render_template('airline_staff_add_airplane.html')

@app.route('/airline_staff_add_airport')
def airline_staff_add_airport():
	return render_template('airline_staff_add_airport.html')

@app.route('/airline_staff_view_booking_agents')
def airline_staff_view_booking_agents():
	return render_template('airline_staff_view_booking_agents.html')

@app.route('/airline_staff_view_frequent_customers')
def airline_staff_view_frequent_customers():
	return render_template('airline_staff_view_frequent_customers.html')

@app.route('/airline_staff_view_reports')
def airline_staff_view_reports():
	return render_template('airline_staff_view_reports.html')

@app.route('/airline_staff_comparison_of_revenue_earned')
def airline_staff_comparison_of_revenue_earned():
	return render_template('airline_staff_comparison_of_revenue_earned.html')

@app.route('/airline_staff_view_top_destinations')
def airline_staff_view_top_destinations():
	return render_template('airline_staff_view_top_destinations.html')

	
"""
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
"""
@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
