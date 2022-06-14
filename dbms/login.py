from flask import Flask, render_template, request, redirect, session, flash, url_for
from functools import wraps
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sanju@123'
app.config['MYSQL_DB'] = 'cafeteria2'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
@app.route('/')
def start():
    return render_template("front page.html")
@app.route('/login', methods=['POST', 'GET'])
def login():
    status = True
   # connection = get_sql_connection()
    if request.method == 'POST':
        email = request.form["email"]
        pwd = request.form["upass"]
        cur = mysql.connection.cursor()
        cur.execute("select * from customer where c_email=%s and c_pswd=%s", (email, pwd))
        data = cur.fetchone()
        if data:
            session['logged_in'] = True
            session['username'] = data["c_user_name"]
            flash('Login Successfully', 'success')
            return redirect('home')
        else:
            flash('Invalid Login. Try Again', 'danger')
    return render_template("login.html")


# check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return redirect(url_for('login'))

    return wrap


# Registration
@app.route('/reg', methods=['POST', 'GET'])
def reg():
    status = False
   # connection = get_sql_connection()
    if request.method == 'POST':
        name = request.form["uname"]
        email = request.form["email"]
        pwd = request.form["upass"]
        cur = mysql.connection.cursor()
        cur.execute("insert into customer(c_user_name,c_pswd,c_email) values(%s,%s,%s)", (name, pwd, email))
        mysql.connection.commit()
        cur.close()
        flash('Registration Successfully. Login Here...', 'success')
        return redirect('login')
    return render_template("reg.html", status=status)


@app.route("/logout")
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/adlogin', methods=['GET', 'POST'])
def loginad():
    #connection = get_sql_connection()
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor()
        #cursor = mysql.cursors.DictCursor
        cursor.execute('SELECT * FROM manager WHERE m_user_name = %s AND m_pswd = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True

            session['username'] = account["m_user_name"]
            # Redirect to home page
            return redirect(url_for('Index'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'''
    # Show the login form with message (if any)
    return render_template('adlogin.html', msg=msg)


'''@app.route("/register", methods=["POST", "GET"])
def register():
    connection = get_sql_connection()
    if request.method == "POST":
        details = request.form
        firstName = details['firstname']
        username = details['username']
        tv3 = details["pass"]
        tv4 = details["phone"]
        tv5 = details["address"]
        cur = connection.cursor()
        cur.execute(
            "INSERT INTO customer(c_id,c_name,c_user_name,c_pswd,c_phone,c_add) VALUES (DEFAULT,%s,%s,%s,%s,%s)",
            (firstName, username, tv3, tv4, tv5))
        connection.commit()
        cur.close()
    return render_template('register.html')'''



@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("main.html")
@app.route('/menu', methods=['GET', 'POST'])
def menu():
    return render_template("store.html")
@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")

@app.route('/')
def Index():
   # connection = get_sql_connection()
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM food")
    data = cur.fetchall()
    cur.close()




    return render_template('index2.html', students=data )



@app.route('/insert', methods = ['POST'])
def insert():
   # connection = get_sql_connection()
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        price = request.form['price']
        type = request.form['type']
        description = request.form['description']
        catID = request.form['catID']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO food (f_name, price, f_type,f_description,cat_id) VALUES (%s,%s,%s,%s,%s)", (name, price, type,description,catID))
        mysql.connection.commit()
        return redirect(url_for('Index'))




@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
   # connection = get_sql_connection()
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM food WHERE f_id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))





@app.route('/update',methods=['POST','GET'])
def update():
    #connection = get_sql_connection()
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        price = request.form['price']
        type = request.form['type']
        description = request.form['description']
        catID = request.form['catID']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE food
               SET f_name=%s, price=%s, f_type=%s,f_description=%s,cat_id=%s
               WHERE f_id=%s
            """, (name, price, type, description,catID,id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))





if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
